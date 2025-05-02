#Validar se é final de semana ou dia útil

dia_semana = input("Digite o dia da semana: ").lower()

if dia_semana == "sábado" or dia_semana == "domingo":
    print("É fim de semana! Vamos avançando em python!!!!")
else:
    print("É dia útil , vamos trabalhar !!!!")
    
print("Fim do programa")