def calculo_gorjeta(valor_conta, porcentagem_gorjeta):
    """
    Calcula o valor da gorjeta com base no valor da conta e na porcentagem informada.

    Parâmetros:
        valor_conta (float): O valor total da conta.
        porcentagem_gorjeta (float): A porcentagem da gorjeta.

    Retorna:
        float: O valor da gorjeta arredondado para 2 casas decimais.
    """
    gorjeta = valor_conta * (porcentagem_gorjeta / 100)
    return round(gorjeta, 2)


def valor_total(valor_conta, valor_gorjeta):
    """
    Calcula o valor total a ser pago, somando a conta com a gorjeta.

    Parâmetros:
        valor_conta (float): O valor da conta.
        valor_gorjeta (float): O valor da gorjeta.

    Retorna:
        float: O valor total a ser pago.
    """
    return round(valor_conta + valor_gorjeta, 2)


def solicitar_valor_float(mensagem):
    """
    Solicita um número decimal ao usuário, validando a entrada.

    Parâmetros:
        mensagem (str): Mensagem exibida ao solicitar a entrada.

    Retorna:
        float: Valor inserido pelo usuário.
    """
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um número válido (use ponto para decimais).")


def main():
    """
    Função principal que executa o programa:
    - Solicita os valores ao usuário,
    - Calcula a gorjeta e o total,
    - Exibe os resultados formatados.
    """
    print("=== Calculadora de Gorjeta ===\n")

    total_conta = solicitar_valor_float("Informe o total da conta: R$ ")
    porcentagem = solicitar_valor_float("Informe a porcentagem da gorjeta: ")

    valor_gorjeta = calculo_gorjeta(total_conta, porcentagem)
    total_a_pagar = valor_total(total_conta, valor_gorjeta)

    print(f"\nPara uma conta de R$ {total_conta:.2f}, a gorjeta de {porcentagem}% equivale a R$ {valor_gorjeta:.2f}.")
    print(f"Valor total a pagar (conta + gorjeta): R$ {total_a_pagar:.2f}")


# Execução direta do script
if __name__ == "__main__":
    main()
