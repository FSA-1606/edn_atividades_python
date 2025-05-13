#Classificar conforme a idade se a pessoa é:  idosa, adulta, adolescente, criança ou bebê

idade = int(input("Informe aqui a sua idade: "))

if idade >= 65:
    print("Você é um idoso e experiente.")
elif idade >=18:
    print("Você é um adulto, seja responsável.")
elif idade >=12:
    print("Você é um adolescente, aproveite com parcimonia.")
elif idade >= 3:
    print("Você é uma criança, divirta-se ao máximo.")
else:
    print("Você é um bebê, em desenvolvimento.")

print("Fim do programa")