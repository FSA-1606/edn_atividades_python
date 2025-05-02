#Calcular valor final do produto com desconto

valor_prod = float (input ("Digite valor do produto: "))
valor_desc = float (input ("Digite o valor do desconto: "))

valor_final = (valor_prod) - (valor_prod * valor_desc/100)

print (f'O valor do produto com desconto de {valor_desc}% será de R$ {valor_final}')

print("Fim do programa")

