#Conversor de Temperatura - Celsius(°C) para Fahrenheit (32 °C × 9/5) + 32
# Fahrenheit (F) para Celsius (32 °F − 32) × 5/9 = 0 °C

celsius = float(input("Digite a temperatura em Celsius: "))
fahrenheit = (celsius * 9/5) +32
print(f"{celsius} ºC equivale a {fahrenheit} ºF")

fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
celsius = (fahrenheit - 32) * 5/9
print(f"{fahrenheit} ºF equivale a {celsius} ºC")

print("Fim do programa")