#Calcular media de notas dos alunos

# Registrar as notas dos alunos
notas = []
numero_de_alunos = 0

while True:
    entrada = input("Digite a nota do aluno (ou escreva 'fim' para encerrar): ")

    # Verifica se o usuário quer encerrar
    if entrada.lower() == 'fim':
        break

    try:
        nota = float(entrada)

        if 0 <= nota <= 10:
            notas.append(nota)
            numero_de_alunos += 1
        else:
            print("Nota inválida. Digite um valor entre 0 e 10!")
    
    except ValueError:
        print("Entrada inválida. Por favor, digite um número entre 0 e 10 ou 'fim'.")

# Calcula e exibe a média
if numero_de_alunos > 0:
    media = sum(notas) / numero_de_alunos
    print(f"\nMédia da turma: {media:.2f}")
    print(f"Total de alunos registrados: {numero_de_alunos}")
else:
    print("\nNenhuma nota foi registrada.")