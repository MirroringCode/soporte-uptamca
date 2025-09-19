from flask_restful import Resource, reqparse
from common.validator import (
    validate_required,
    validate_length,
    validate_numeric
)
from models import User, Rol
from db import db

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True)
post_parser.add_argument('password', type=str, required=True)
post_parser.add_argument('confirm_password', type=str, required=True)
post_parser.add_argument('id_rol', type=int, required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('username', type=str, required=False),
put_parser.add_argument('password', type=str, required=False)
put_parser.add_argument('id_rol', type=int, required=False),

password_parser = reqparse.RequestParser()
password_parser.add_argument('new_password', type=str, required=True)
password_parser.add_argument('confirm_new_password', type=str, required=True)

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
            errores = []
            
            try:
                validate_required(args['username'])
                validate_length(args['username'], min_length=2, max_length=100)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['password'])
                validate_length(args['password'], min_length=4, max_length=100)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['confirm_password'])
            except ValueError as e:
                errores.append(str(e))
            
            try:
                validate_required(args['id_rol'])
                validate_numeric(args['id_rol'])
            except ValueError as e:
                errores.append(str(e))


            rol = Rol.query.get(args['id_rol'])
            if not rol:
                errores.append('El rol especificado no existe')

            # Verificar si usuario ya existe
            if User.query.filter_by(username=args['username']).first():
                errores.append('Este usuario ya existe')

            if args['password'] != args['confirm_password']:
                errores.append('Las contraseñas no coinciden')
            


            if errores:
                return {
                    'success': False,
                    'errors': errores,
                    'message': 'Hubo un problema al registrar el nuevo usuario'
                }

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
                errores = []
                if not usuario:
                    return {
                        'success': False,
                        'message': 'Usuario no encontrado'
                    }, 404

                try:
                    validate_required(args['username'])
                    validate_length(args['username'], 2, 100)
                except ValueError as e:
                    errores.append(str(e))
                
                try:
                    validate_required(args['id_rol'])
                    validate_numeric(args['id_rol'])
                except ValueError as e:
                    errores.append(str(e))

                if args['username'] and args['username'] != usuario.username:
                    if User.query.filter_by(username=args['username']).filter(User.id != user_id).first():
                        errores.append('El nombre de usuario ya está en uso')
                    usuario.username = args['username']

                rol = Rol.query.get(args['id_rol'])
                if not rol:
                    errores.append('El rol especificado no existe')
                   

                if errores:
                    return {
                        'success': False,
                        'errors': errores,
                        'message': 'Hubo un problema al editar la información del usuario'
                    }, 400


                if args['id_rol']:
                    usuario.id_rol = args['id_rol']

                db.session.commit()

                return {
                    'success': True,
                    'message': 'Información de usuario actualizado exitosamente',
                    'data': usuario.to_dict()
                }, 200

            except Exception as e:
                db.session.rollback()
                return {
                    'success': False,
                    'error': str(e),
                    'message': 'Error al actualizar la información de usuario'
                }, 500
            
        def delete(self, user_id):
            try:
                user = User.query.get(user_id)
                if not user:
                    return {
                        'success': False,
                        'message': 'No se encontró este usuario'
                    }, 404


                if user.soportes and len(user.soportes) > 0:
                    return {
                        'success': False,
                        'message': 'Hay soportes vinculados a este usuario y no se puede borrar'
                    }, 400

                db.session.delete(user)
                db.session.commit()

                return {
                    'success': True,
                    'message': 'Se ha borrado información del usuario exitosamente'
                }, 200
            except Exception as e:
                return {
                    'success': False,
                    'message': 'Hubo un error al borrar la información de este usuario'
                }, 500


class PasswordResource(Resource):
    def put(self, user_id):
        """ Reiniciar contraseña con confirmación """
        try:
            args = password_parser.parse_args()
            errores = []
            usuario = User.query.get(user_id)
            if not usuario:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, 404

            try:
                validate_required(args['new_password'])
                validate_length(args['new_password'], min_length=4, max_length=100)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['confirm_new_password'])
            except ValueError as e:
                errores.append(str(e))

            if args['new_password'] != args['confirm_new_password']:
                errores.append('Las contraseñas no coinciden')
            
            if errores:
                return {
                    'success': False,
                    'errors': errores,
                    'message': 'Ha habido un problema reiniciando la clave'
                }, 400
            
            usuario.password = args['new_password']
            db.session.commit()

            return {
                'success': True,
                'message': 'Contraseña reiniciada exitosamente'
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'success': True,
                'error': str(e),
                'message': 'Ha habido un problema reiniciando la clave'
            }, 500
