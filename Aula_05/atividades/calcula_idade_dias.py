#Calcular idade da pessoa em dias 

import datetime #Imprtar função do python 

def calcular_idade_em_dias(ano_nascimento):
    """
    Calcula a idade aproximada de uma pessoa em dias.

    Parâmetros:
        ano_nascimento (int): Ano de nascimento da pessoa.

    Retorna:
        int: Idade aproximada em dias (sem considerar anos bissextos).
    """
    ano_atual = datetime.datetime.now().year
    idade_anos = ano_atual - ano_nascimento
    idade_dias = idade_anos * 365  # Aproximação, não considera anos bissextos
    return idade_dias

def main():
    try:
        ano = int(input("Digite o ano de nascimento: "))

        ano_atual = datetime.datetime.now().year
        if ano > ano_atual:
            print("Erro: Ano de nascimento não pode ser no futuro.")
        elif ano < 1800:
            print("Erro: Ano de nascimento muito distante. Verifique o valor digitado.")
        else:
            dias = calcular_idade_em_dias(ano)
            print(f"Sua idade aproximada em dias é: {dias} dias.")

    except ValueError:
        print("Erro: Digite um ano válido em formato numérico (ex: 1980).")

if __name__ == "__main__":
    main()




 