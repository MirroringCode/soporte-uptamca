from flask_restful import Resource, reqparse
from models import Personal


parser = reqparse.RequestParser()
parser.add_argument() 

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

    def post(self):
