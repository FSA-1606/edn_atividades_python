#Calcular IMC Índice de Massa Corporal - Formula : peso / altura ** 2

altura = float(input("Digite a sua altura em metros: "))
peso = float(input("Digite seu peso em kg :"))

imc = peso / (altura ** 2)

#print(f"Seu IMC é {imc:.2f}")

# Classificação do IMC

if imc < 18.5:
    classificacao = "Abaixo do peso"
elif imc < 25:
    classificacao = "Peso normal"
elif imc < 30:
    classificacao = "Sobrepeso"
elif imc < 35:
    classificacao = "Obesidade grau 1"
elif imc < 40:
    classificacao = "Obesidade grau 2"
else:
    classificacao = "Obesidade grau 3"
    
#print(f'Seu IMC esta classificado como {classificacao}')
print(f"Seu IMC é {imc:.2f} e está classificado como: {classificacao}")

print("Fim do programa")

