def calculo_gorjeta(valor_conta, porcentagem_gorjeta):
    """
    Calcula o valor da gorjeta baseado no total da conta e na porcentagem informada.

    Parâmetros:
        valor_conta (float): Valor total da conta.
        porcentagem_gorjeta (float): Porcentagem da gorjeta.

    Retorna:
        float: Valor da gorjeta arredondado para 2 casas decimais.
    """
    gorjeta = valor_conta * (porcentagem_gorjeta / 100)
    return round(gorjeta, 2)


def solicitar_valor_float(mensagem):
    """
    Solicita ao usuário um número de ponto flutuante, com validação.

    Parâmetros:
        mensagem (str): Texto a ser exibido ao solicitar o valor.

    Retorna:
        float: Valor numérico inserido pelo usuário.
    """
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número válido (use ponto para decimais).")


def main():
    """
    Função principal do programa. Solicita os dados, calcula a gorjeta e exibe o resultado formatado.
    """
    print("=== Calculadora de Gorjeta ===")
    
    total_conta = solicitar_valor_float("Informe o total da conta: R$ ")
    porcentagem = solicitar_valor_float("Informe a porcentagem da gorjeta: ")

    valor_gorjeta = calculo_gorjeta(total_conta, porcentagem)

    print(f"\nPara uma conta de R$ {total_conta:.2f}, a gorjeta de {porcentagem:.1f}% é R$ {valor_gorjeta:.2f}")


# Execução direta
if __name__ == "__main__":
    main()
