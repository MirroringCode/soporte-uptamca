from flask_restful import Resource, reqparse
from models import Personal
from db import db


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('cedula', type=str, required=True, help='Debe indicar la cédula del empleado')
parser.add_argument('nombre', type=str, required=True, help='Debe indicar el nombre del empleado') 
parser.add_argument('apellido', type=str, required=True, help='Debe indicar el apellido del empleado')
parser.add_argument('id_departamento', type=int, required=True, help='Debe indicar a que departamento pertenece el empleado') 

""" PENDIENTE POR HACER
- """

class PersonalResource(Resource):
    """ Método para traer todos los empleados existentes en base de datos """
    def get(self):
        try:
            # Hace consulta a la base de datos
            empleados = Personal.query.all()

            # Si todo sale bien devuelve respuesta en formato JSON
            return {
                'success': True,
                'data': [e.to_dict() for e in empleados],
                'count': len(empleados),
                'message': 'Lista de empleados obtenida exitosamente'
            }, 200
        except Exception as e:
            # Si ocurre un error, envía respuesta en formato JSON en conjunto con el error
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error obteniendo la lista de empleados' 
            }, 500

    """ Método para crear un nuevo empleado """
    def post(self):
        try:
            args = parser.parse_args()
            
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
            

class EmpleadoResource(Resource):
    def put(self, personal_id):
        empleado = Personal.query.filter(personal_id).first()
        return {
            'message': f'Actualizando empleado con ID {personal_id}'
        }