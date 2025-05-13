import requests

def obter_usuario_aleatorio():
    url = "https://randomuser.me/api"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança exceção para códigos de erro HTTP

        data = response.json()
        user = data['results'][0]

        nome = f"{user['name']['title']} {user['name']['first']} {user['name']['last']}"
        email = user['email']
        pais = user['location']['country']

        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"País: {pais}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição à API: {e}")

if __name__ == "__main__":
    obter_usuario_aleatorio()
