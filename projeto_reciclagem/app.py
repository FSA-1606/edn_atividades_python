from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import sqlite3
import json
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from sklearn.cluster import KMeans
import numpy as np
from authlib.integrations.flask_client import OAuth
import secrets

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
bcrypt = Bcrypt(app)

# Configuração do OAuth para Google
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='SEU_GOOGLE_CLIENT_ID',  # Substitua pelo Client ID do Google
    client_secret='SEU_GOOGLE_CLIENT_SECRET',  # Substitua pelo Client Secret do Google
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    redirect_uri='http://localhost:5000/login/google/callback',
    client_kwargs={'scope': 'email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
)

# Inicializa o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT,
                    role TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    google_id TEXT UNIQUE)''')
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
    if 'user_id' in session:
        return redirect(url_for('dashboard', user_id=session['user_id']))
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
            flash('Registro concluído com sucesso! Por favor, adicione sua localização para melhor experiência.', 'info')
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
        if user and user[2] and bcrypt.check_password_hash(user[2], password):
            session['user_id'] = user[0]
            if user[4] is None or user[5] is None:
                flash('Sua localização não foi informada. Atualize-a no painel para otimizar rotas.', 'info')
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard', user_id=user[0]))
        else:
            flash('Credenciais inválidas!', 'error')
    return render_template('login.html')

# Rota de login com Google
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('login_google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

# Callback do Google OAuth
@app.route('/login/google/callback')
def login_google_callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    google_id = user_info['sub']
    email = user_info['email']

    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE google_id = ? OR username = ?', (google_id, email))
    user = c.fetchone()

    if user:
        session['user_id'] = user[0]
        flash('Login com Google realizado com sucesso!', 'success')
    else:
        # Criar um novo usuário
        username = email
        role = 'doador'  # Papel padrão para novos usuários via Google
        try:
            c.execute('INSERT INTO users (username, role, google_id) VALUES (?, ?, ?)',
                      (username, role, google_id))
            conn.commit()
            c.execute('SELECT * FROM users WHERE google_id = ?', (google_id,))
            user = c.fetchone()
            session['user_id'] = user[0]
            flash('Conta criada e login realizado com sucesso via Google!', 'success')
        except sqlite3.IntegrityError:
            flash('Erro ao criar conta com Google. Tente outro método de login.', 'error')
            return redirect(url_for('login'))

    conn.close()
    return redirect(url_for('dashboard', user_id=session['user_id']))

# Rota para redefinir senha
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        
        if len(new_password) < 6:
            flash('A nova senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('reset_password.html')

        conn = sqlite3.connect('recyclable_platform.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        
        if user:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            c.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
            conn.commit()
            flash(f'Senha redefinida com sucesso! Sua nova senha é: {new_password}', 'success')
            return redirect(url_for('login'))
        else:
            flash('Usuário não encontrado!', 'error')
        
        conn.close()
    return render_template('reset_password.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('index'))

# Rota do painel
@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Por favor, faça login para acessar o painel.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    materials = []
    if user[3] == 'doador':
        c.execute('SELECT * FROM materials WHERE user_id = ?', (user_id,))
        materials = c.fetchall()
    
    doadores = []
    doadores_sem_localizacao = []
    if user[3] == 'coletor':
        c.execute('SELECT id, username, latitude, longitude FROM users WHERE role = "doador" AND latitude IS NOT NULL AND longitude IS NOT NULL')
        doadores = c.fetchall()
        c.execute('SELECT id, username FROM users WHERE role = "doador" AND (latitude IS NULL OR longitude IS NULL)')
        doadores_sem_localizacao = c.fetchall()
    
    conn.close()
    return render_template('dashboard.html', user=user, materials=materials, doadores=doadores, doadores_sem_localizacao=doadores_sem_localizacao)

# Rota para atualizar localização
@app.route('/update_location/<int:user_id>', methods=['GET', 'POST'])
def update_location(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Por favor, faça login para atualizar sua localização.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()

    if request.method == 'POST':
        latitude = float(request.form['latitude']) if request.form['latitude'] else None
        longitude = float(request.form['longitude']) if request.form['longitude'] else None

        if latitude is None or longitude is None:
            flash('Por favor, informe latitude e longitude válidas.', 'error')
        else:
            c.execute('UPDATE users SET latitude = ?, longitude = ? WHERE id = ?', (latitude, longitude, user_id))
            conn.commit()
            flash('Localização atualizada com sucesso!', 'success')
            return redirect(url_for('dashboard', user_id=user_id))

    conn.close()
    return render_template('update_location.html', user=user)

# Rota para remover material
@app.route('/remove_material/<int:user_id>/<int:material_id>', methods=['POST'])
def remove_material(user_id, material_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Por favor, faça login para remover materiais.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if user[0] != 'doador':
        flash('Apenas doadores podem remover materiais.', 'error')
        conn.close()
        return redirect(url_for('dashboard', user_id=user_id))

    c.execute('DELETE FROM materials WHERE id = ? AND user_id = ?', (material_id, user_id))
    conn.commit()
    conn.close()
    flash('Material removido com sucesso!', 'success')
    return redirect(url_for('dashboard', user_id=user_id))

# Rota para visualizar detalhes de um doador
@app.route('/doador_details/<int:user_id>/<int:doador_id>')
def doador_details(user_id, doador_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Por favor, faça login para visualizar detalhes.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if user[0] != 'coletor':
        flash('Apenas coletores podem visualizar detalhes de doadores.', 'error')
        conn.close()
        return redirect(url_for('dashboard', user_id=user_id))

    c.execute('SELECT username, latitude, longitude FROM users WHERE id = ?', (doador_id,))
    doador = c.fetchone()
    if not doador:
        flash('Doador não encontrado.', 'error')
        conn.close()
        return redirect(url_for('dashboard', user_id=user_id))

    c.execute('SELECT material_type, quantity FROM materials WHERE user_id = ?', (doador_id,))
    materiais = c.fetchall()
    conn.close()
    
    return render_template('doador_details.html', doador=doador, materiais=materiais, user_id=user_id)

# Rota para adicionar material
@app.route('/add_material/<int:user_id>', methods=['GET', 'POST'])
def add_material(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Por favor, faça login para adicionar materiais.', 'error')
        return redirect(url_for('login'))

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
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Por favor, faça login para visualizar o mapa.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT id, username, latitude, longitude, role FROM users WHERE latitude IS NOT NULL AND longitude IS NOT NULL')
    users = c.fetchall()
    conn.close()

    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [user[3], user[2]]
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

# Otimização de rota com clustering
@app.route('/optimize_route/<int:user_id>')
def optimize_route(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Por favor, faça login para otimizar a rota.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('recyclable_platform.db')
    c = conn.cursor()
    c.execute('SELECT id, latitude, longitude FROM users WHERE role = "doador" AND latitude IS NOT NULL AND longitude IS NOT NULL')
    doadores = c.fetchall()
    c.execute('SELECT latitude, longitude FROM users WHERE id = ?', (user_id,))
    coletor = c.fetchone()
    conn.close()

    if not doadores or not coletor:
        flash('Dados de localização insuficientes para otimização de rota. Peça aos doadores para atualizarem suas localizações no painel.', 'error')
        return redirect(url_for('dashboard', user_id=user_id))

    coords = np.array([(d[1], d[2]) for d in doadores])
    num_doadores = len(doadores)
    num_clusters = max(2, min(num_doadores // 2, 3))
    if num_doadores < 2:
        flash('Pelo menos 2 doadores com localização são necessários para otimizar a rota.', 'error')
        return redirect(url_for('dashboard', user_id=user_id))

    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(coords)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    clustered_doadores = [[] for _ in range(num_clusters)]
    for idx, label in enumerate(labels):
        clustered_doadores[label].append(doadores[idx])

    routes = []
    for cluster_idx, cluster in enumerate(clustered_doadores):
        if not cluster:
            continue

        cluster_coords = [(centroids[cluster_idx][0], centroids[cluster_idx][1])]
        cluster_coords.extend([(d[1], d[2]) for d in cluster])

        n = len(cluster_coords)
        distance_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    lat1, lon1 = cluster_coords[i]
                    lat2, lon2 = cluster_coords[j]
                    distance_matrix[i][j] = int(((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5 * 100000)

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
                if node != 0:
                    route.append(cluster[node-1][0])
                index = solution.Value(routing.NextVar(index))
            routes.append(route)

    if routes:
        flash(f'Rota otimizada por clusters: {routes}', 'success')
    else:
        flash('Não foi possível calcular a rota.', 'error')
    
    return redirect(url_for('dashboard', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)