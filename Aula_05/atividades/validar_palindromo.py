# Validar um palindromo 
#Obs: Frase ou palavra que se pode ler, indiferentemente, da esquerda para a direita ou vice-versa.

def validar_palindromo(texto):
    """
    Verifica se o texto é palíndromo (ignora espaços, pontuação e diferenciação de maiúsculas/minúsculas).
    
    Param:
        texto (str): A string que será verificada.
    
    Retorna:
        bool: True se for palíndromo, False caso contrário.
    """
    # Filtrando apenas letras e números e convertendo para minúsculas
    texto_processado = ''.join(caractere.lower() for caractere in texto if caractere.isalnum())

    # Verificando se o texto processado é igual ao seu reverso
    return texto_processado == texto_processado[::-1]


def main():
    texto = input("Digite uma palavra ou frase: ")
    resultado = validar_palindromo(texto)

    # Mensagem de resposta baseada no resultado
    resposta = "Sim" if resultado else "Não"
    print(f"'{texto}' é um palíndromo? {resposta}")


if __name__ == "__main__":
    main()
