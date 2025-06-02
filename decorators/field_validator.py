from functools import wraps
from validate import is_valid_password, is_valid_email

def validate_input(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        email = self.email_input.text()
        password = self.password_input.text()

        # Validação do e-mail
        if not is_valid_email(email):
            self.show_message("Erro", "O e-mail fornecido não é válido.", "error")
            return

        # Validação da senha
        if not is_valid_password(password):
            self.show_message("Erro", "A senha deve ter pelo menos 8 caracteres, incluindo letras e números.", "error")
            return

        # Se as validações passarem, chama a função original
        return func(self, *args, **kwargs)

    return wrapper
