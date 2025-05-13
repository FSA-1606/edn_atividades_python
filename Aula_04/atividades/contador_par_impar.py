"""
Programa para contar quantos números pares e ímpares são digitados pelo usuário.
Apenas números inteiros positivos são considerados válidos.
O programa exibe o total de entradas válidas e o percentual de pares e ímpares.
"""

def classificar_numero(numero):
    """
    Classifica o número como par ou ímpar.

    Args:
        numero (int): Número inteiro positivo.

    Returns:
        str: 'par' se o número for par, 'ímpar' se for ímpar.
    """
    return 'par' if numero % 2 == 0 else 'ímpar'


def exibir_resultados(total, pares, impares):
    """
    Exibe o resultado final da contagem de números.

    Args:
        total (int): Total de números válidos digitados.
        pares (int): Quantidade de números pares.
        impares (int): Quantidade de números ímpares.
    """
    print("\nResultado:")
    print(f"Total de números válidos: {total}")
    print(f"Números pares: {pares} ({(pares / total * 100):.1f}%)")
    print(f"Números ímpares: {impares} ({(impares / total * 100):.1f}%)")


def main():
    """
    Função principal que executa a leitura dos números e contabiliza os pares e ímpares.
    """
    pares = 0
    impares = 0
    total = 0

    while True:
        entrada = input("Digite um número inteiro positivo (ou 'fim' para encerrar): ")

        if entrada.strip().lower() == 'fim':
            print("\nEncerrado com sucesso!")
            break

        try:
            numero = int(entrada)

            if numero < 0:
                print("Número negativo ignorado. Digite apenas números inteiros positivos.")
                continue

            total += 1
            tipo = classificar_numero(numero)

            if tipo == 'par':
                pares += 1
            else:
                impares += 1

            print(f"O número {numero} é {tipo}.")

        except ValueError:
            print("Erro: Digite apenas números inteiros positivos ou 'fim' para encerrar.")

    if total > 0:
        exibir_resultados(total, pares, impares)
    else:
        print("Nenhum número válido foi digitado.")


# Executa o programa
if __name__ == "__main__":
    main()
