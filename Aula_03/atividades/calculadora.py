#Criar uma calculadora simples 
while True:
    print("\n### Calculadora Simples ###")
    print("Escolha a operação:")
    print("1. Adição (+)")
    print("2. Subtração (-)")
    print("3. Multiplicação (*)")
    print("4. Divisão (/)")
    print("5. Sair")

    escolha = input("Digite o número da operação desejada: ")

    if escolha == '5':
        print("Encerrando a calculadora. Até logo!")
        break

    if escolha not in ('1', '2', '3', '4'):
        print("Opção inválida. Tente novamente.")
        continue

    try:
        num1 = float(input("Digite o primeiro número: "))
        num2 = float(input("Digite o segundo número: "))
    except ValueError:
        print("Entrada inválida. Por favor, digite números válidos.")
        continue

    if escolha == '1':
        resultado = num1 + num2
        operador = '+'
    elif escolha == '2':
        resultado = num1 - num2
        operador = '-'
    elif escolha == '3':
        resultado = num1 * num2
        operador = '*'
    elif escolha == '4':
        if num2 == 0:
            print("Erro: divisão por zero.")
            continue
        resultado = num1 / num2
        operador = '/'

    print(f"Resultado: {num1} {operador} {num2} = {resultado}")
