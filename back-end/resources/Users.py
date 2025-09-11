from flask_restful import Resource, reqparse
from models import User
from db import db

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('id_rol', type=int, required=True)


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

    def post(self):
        """Crear nuevo usuario"""
        try:
            args = parser.parse_args()
            
            # Verificar si usuario ya existe
            if User.query.filter_by(username=args['username']).first():
                return {
                    'success': False,
                    'message': 'El usuario ya existe'
                }, 400
            
            nuevo_usuario = User(
                username=args['username'],
                password=args['password'],  # Se hashea automáticamente
                id_rol=args['id_rol']
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            return {
                'success': True,
                'data': nuevo_usuario.to_dict(),
                'message': 'Usuario creado exitosamente'
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Error al crear usuario'
            }, 500
