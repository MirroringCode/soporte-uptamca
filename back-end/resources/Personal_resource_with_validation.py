# Puedes poner estas funciones arriba en el mismo archivo o en un archivo utils/validators.py
def validate_length(value, min_length=1, max_length=100):
    if value is None or not (min_length <= len(value.strip()) <= max_length):
        raise ValueError(f"El campo debe tener entre {min_length} y {max_length} caracteres")
    return value.strip()

def validate_numeric(value):
    if value is None or not str(value).isdigit():
        raise ValueError("El campo debe ser numérico")
    return value

def validate_required(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError("Este campo es requerido")
    return value

# ...existing code...

class PersonalResource(Resource):
    def post(self):
        try:
            args = post_parser.parse_args()
            errores = []

            # Validaciones personalizadas
            try:
                cedula = validate_required(args['cedula'])
                cedula = validate_length(cedula, min_length=6, max_length=20)
                cedula = validate_numeric(cedula)
                nombre = validate_required(args['nombre'])
                nombre = validate_length(nombre, min_length=2, max_length=50)
                apellido = validate_required(args['apellido'])
                apellido = validate_length(apellido, min_length=2, max_length=50)
            except ValueError as ve:
                errores.append(str(ve))

            if Personal.query.filter_by(cedula=args['cedula']).first():
                errores.append('Ya existe un empleado con esa cédula')

            departamento = Departamento.query.get(args['id_departamento'])
            if not departamento:
                errores.append('El departamento especificado no existe') 

            if errores:
                return {
                    'success': False,
                    'errors': errores,
                    'message':'Ha habido un problema registrando al nuevo empleado'
                }, 400

            nuevo_empleado = Personal(
                cedula=args['cedula'],
                nombre=args['nombre'],
                apellido=args['apellido'],
                id_departamento=args['id_departamento']
            )
            
            db.session.add(nuevo_empleado)
            db.session.commit()

            return {
                'success': True,
                'message': 'Empleado creado exitosamente',
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error creando el empleado'
            }, 500
# ...existing code...