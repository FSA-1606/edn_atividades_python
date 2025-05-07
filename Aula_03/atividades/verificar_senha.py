#Criar um programa de verificação de senhas devem ser fortes.
# Deve ter tamanho mínimo de 8 caracteres entre eles : especiais, números e letras. Uma das letras deve ser maiúscula. 

def verificar_senha_forte(senha):
    """
   Função verifica se uma senha atende aos critérios de segurança.

    Args:
        senha (str): A senha a ser verificada.

    Returns:
        tuple: Uma tupla contendo (bool, str).
               O booleano indica se a senha é forte (True) ou não (False).
               A string contém uma mensagem explicando o resultado.
    """
    # Define os caracteres especiais permitidos
    caracteres_especiais = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # 1. Verifica se a senha tem pelo menos 8 caracteres
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."

    # 2. Verifica se contém pelo menos uma letra maiúscula
    if not any(c.isupper() for c in senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula."

    # 3. Verifica se contém pelo menos uma letra minúscula
    if not any(c.islower() for c in senha):
        return False, "A senha deve conter pelo menos uma letra minúscula."

    # 4. Verifica se contém pelo menos um número
    if not any(c.isdigit() for c in senha):
        return False, "A senha deve conter pelo menos um número."

    # 5. Verifica se contém pelo menos um caractere especial
    if not any(c in caracteres_especiais for c in senha):
        return False, f"A senha deve conter pelo menos um caractere especial. Caracteres permitidos: {caracteres_especiais}"

    # Se passou por todas as verificações, a senha é forte
    return True, "A senha é forte!"

def main():
    """
    Função principal para interagir com o usuário e verificar senhas.
    """
    print("Verificador de Força de Senha")
    print("Digite 'sair' a qualquer momento para encerrar o programa.")
    print("-" * 30)

    while True:
        senha_digitada = input("Digite uma senha: ")

        # Verifica se o usuário quer sair
        if senha_digitada.lower() == 'sair':
            print("Programa encerrado.")
            break

        # Chama a função de verificação de senha
        eh_forte, mensagem = verificar_senha_forte(senha_digitada)

        # Exibe o resultado
        print(f"Resultado: {mensagem}\n")

if __name__ == "__main__":
    main()