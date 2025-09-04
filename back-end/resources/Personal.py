from flask_restful import Resource
from models import Personal


class PersonalResource(Resource):
    def get(self):
        try:
            empleados = Personal.query.all()

            return {
                'success': True,
                'data': [e.to_dict() for e in empleados],
                'count': len(empleados),
                'message': 'Lista de empleados obtenida exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error obteniendo la lista de empleados' 
            }, 500
