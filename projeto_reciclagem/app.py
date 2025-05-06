from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import sqlite3
import json
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
bcrypt = Bcrypt(app)

# Inicializa o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    material_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

init_db()

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        latitude = float(request.form['latitude']) if request.form['latitude'] else None
        longitude = float(request.form['longitude']) if request.form['longitude'] else None

        # Valida entradas
        if not username or len(password) < 6:
            flash('Nome de usuário é obrigatório e a senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = sqlite3.connect('recyclable_platform.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password, role, latitude, longitude) VALUES (?, ?, ?, ?, ?)',
                      (username, hashed_password, role, latitude, longitude))
            conn.commit()
            flash('Registro concluído com sucesso!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe!', 'error')
        finally:
            conn.close()
    return render_template('register.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('recyclable_platform.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user[2], password):
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard', user_id=user[0]))
        else:
            flash('Credenciais inválidas!', 'error')
    return render_template('login.html')

# Rota do painel
@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    # Busca materiais se o usuário for doador
    materials = []
    if user[3] == 'doador':
        c.execute('SELECT * FROM materials WHERE user_id = ?', (user_id,))
        materials = c.fetchall()
    
    # Busca doadores próximos se o usuário for coletor
    doadores = []
    if user[3] == 'coletor':
        c.execute('SELECT id, username, latitude, longitude FROM users WHERE role = "doador" AND latitude IS NOT NULL AND longitude IS NOT NULL')
        doadores = c.fetchall()
    
    conn.close()
    return render_template('dashboard.html', user=user, materials=materials, doadores=doadores)

# Rota para adicionar material
@app.route('/add_material/<int:user_id>', methods=['GET', 'POST'])
def add_material(user_id):
    if request.method == 'POST':
        material_type = request.form['material_type']
        try:
            quantity = int(request.form['quantity'])
            if quantity <= 0:
                raise ValueError
        except ValueError:
            flash('A quantidade deve ser um número inteiro positivo!', 'error')
            return render_template('add_material.html', user_id=user_id)
        
        conn = sqlite3.connect('recyclable_platform.db')
        c = conn.cursor()
        c.execute('INSERT INTO materials (user_id, material_type, quantity) VALUES (?, ?, ?)',
                  (user_id, material_type, quantity))
        conn.commit()
        conn.close()
        flash('Material adicionado com sucesso!', 'success')
        return redirect(url_for('dashboard', user_id=user_id))
    return render_template('add_material.html', user_id=user_id)

# Rota do mapa
@app.route('/map/<int:user_id>')
def show_map(user_id):
    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT id, username, latitude, longitude, role FROM users WHERE latitude IS NOT NULL AND longitude IS NOT NULL')
    users = c.fetchall()
    conn.close()

    # Prepara dados GeoJSON para Leaflet
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [user[3], user[2]]  # [longitude, latitude]
                },
                "properties": {
                    "username": user[1],
                    "role": user[4],
                    "user_id": user[0]
                }
            } for user in users
        ]
    }
    return render_template('map.html', geojson_data=json.dumps(geojson_data), user_id=user_id)

# Otimização de rota
@app.route('/optimize_route/<int:user_id>')
def optimize_route(user_id):
    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT id, latitude, longitude FROM users WHERE role = "doador" AND latitude IS NOT NULL AND longitude IS NOT NULL')
    doadores = c.fetchall()
    c.execute('SELECT latitude, longitude FROM users WHERE id = ?', (user_id,))
    coletor = c.fetchone()
    conn.close()

    if not doadores or not coletor:
        flash('Dados de localização insuficientes para otimização de rota.', 'error')
        return redirect(url_for('dashboard', user_id=user_id))

    # Matriz de distâncias simples (distância euclidiana para demonstração)
    locations = [(coletor[0], coletor[1])] + [(d[1], d[2]) for d in doadores]
    n = len(locations)
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                lat1, lon1 = locations[i]
                lat2, lon2 = locations[j]
                distance_matrix[i][j] = int(((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5 * 100000)  # Aprox. em metros

    # Solucionador TSP do OR-Tools
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            if node != 0:  # Ignora o ponto inicial
                route.append(doadores[node-1][0])  # ID do usuário
        flash(f'Rota otimizada: Visite doadores com IDs {route}', 'success')
    else:
        flash('Não foi possível calcular a rota.', 'error')
    
    return redirect(url_for('dashboard', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)