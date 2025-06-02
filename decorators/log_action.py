from functools import wraps
from logger import Logger

def log_action(id, acao):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultado = func(*args, **kwargs)
            print('ta dentro do log_action.py', id, acao)
            if id:
                Logger.registrar_acao(id, acao)
            return resultado
        return wrapper
    return decorator
