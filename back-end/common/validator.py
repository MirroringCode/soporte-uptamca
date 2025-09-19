import re
from datetime import datetime

def validate_length(value, min_length=1, max_length=255):
    if value is None:
        raise ValueError('El campo es requerido')
    if not (min_length <= len(value) <= max_length):
        raise ValueError(f'El campo debe tener entre {min_length} y {max_length} caracteres')
    return value

def validate_numeric(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return value
    raise ValueError('Solo puede ingresar números')

def validate_required(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError('Este campo no puede estar vacío')
    return value

def validate_date_format(value, fmt='%Y-%m-%d'):
    try:
        return datetime.strptime(value, fmt)
    except Exception:
        raise ValueError(f'La fecha no coincide con el formato solicitado: {fmt}')
    
def validate_regex(value, pattern, message="formato invalido"):
    if not re.match(value, pattern):
        raise ValueError(message)
    return value