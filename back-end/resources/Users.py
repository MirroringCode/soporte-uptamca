from flask_restful import Resource
from models import User

class UsersResource(Resource):
    def get(self):
        try:
            users = User.query.all()

            return {
                'success': True,
                'data': [u.to_dict() for u in users],
                'count': len(users),
                'message': 'Lista de usuarios obtenidas exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Hubo un error al obtener la lista de usuario'
            }, 500
