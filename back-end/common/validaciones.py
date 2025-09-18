# Puedes poner esto en un archivo utils/validators.py para reutilizar

import re
from datetime import datetime

def validate_length(value, min_length=1, max_length=255):
    if value is None:
        raise ValueError("El campo es requerido")
    if not (min_length <= len(value) <= max_length):
        raise ValueError(f"El campo debe tener entre {min_length} y {max_length} caracteres")
    return value

def validate_numeric(value):
    if value is None or not str(value).isdigit():
        raise ValueError("El campo debe ser numérico")
    return int(value)

def validate_required(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError("Este campo es requerido")
    return value

def validate_date_format(value, fmt='%Y-%m-%d'):
    try:
        return datetime.strptime(value, fmt)
    except Exception:
        raise ValueError(f"La fecha debe tener el formato {fmt}")

def validate_regex(value, pattern, message="Formato inválido"):
    if not re.match(pattern, value):
        raise ValueError(message)
    return value

# Ejemplo de uso en un Resource
class EjemploResource(Resource):
    def post(self):
        args = post_parser.parse_args()
        errores = []
        try:
            nombre = validate_length(args['nombre'], min_length=3, max_length=50)
            cedula = validate_numeric(args['cedula'])
            fecha = validate_date_format(args['fecha'], fmt='%Y-%m-%d')
            # Puedes agregar más validaciones aquí
        except ValueError as e:
            errores.append(str(e))

        if errores:
            return {'success': False, 'errors': errores}, 400

        # Si todo está bien, continúa con la lógica de creación
        # ...