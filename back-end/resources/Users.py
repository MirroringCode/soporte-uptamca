from flask_restful import Resource, reqparse
from models import User
from db import db

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True)
post_parser.add_argument('password', type=str, required=True)
post_parser.add_argument('id_rol', type=int, required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('username', type=str, required=False),
put_parser.add_argument('password', type=str, required=False)
put_parser.add_argument('id_rol', type=int, required=False),

class UsersResource(Resource):
    def get(self):
        try:
            users = User.query.all()

            return {
                'success': True,
                'data': [u.to_dict() for u in users] or 'No se encontraron usuarios',
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
            args = post_parser.parse_args()
            
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
        
class UserResource(Resource):
        def put(self, user_id):
            """ Actualizar usuario existente """
            try:
                args = put_parser.parse_args()
                usuario = User.query.get(user_id)
                if not usuario:
                    return {
                        'success': False,
                        'message': 'Usuario no encontrado'
                    }, 404
                
                if args['username'] and args['username'] != usuario.username:
                    if User.query.filter_by(username=args['username']).filter(User.id != user_id).first():
                        return {
                            'success': False,
                            'message': 'El nombre de usuario ya está en uso'
                        }, 400
                    usuario.username = args['username']

                if args['id_rol']:
                    usuario.id_rol = args['id_rol']

                db.session.commit()

                return {
                    'success': True,
                    'message': 'Información de usuario actualizado exitosamente',
                    'data': usuario.to_dict()
                }

            except Exception as e:
                db.session.rollback()
                return {
                    'success': False,
                    'error': str(e),
                    'message': 'Error al actualizar la información de usuario'
                }

class PasswordResource(Resource):
    def put(self, user_id):
        return "Reiniciar contraseña"