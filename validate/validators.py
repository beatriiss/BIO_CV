import re

def is_valid_email(email):
    # Valida o formato do e-mail usando uma expressão regular simples
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    # Valida se a senha tem pelo menos 8 caracteres, com números e letras
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)
