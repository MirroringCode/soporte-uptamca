from flask import make_response, render_template, request
from flask_restful import Resource, reqparse
from common.validator import (
    validate_required,
    validate_length,
    validate_numeric
)
from common.check_htmx_request import is_htmx_request
from models import User, Rol
from db import db

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True)
post_parser.add_argument('password', type=str, required=True)
post_parser.add_argument('confirm_password', type=str, required=True)
post_parser.add_argument('id_rol', type=int, required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('username', type=str, required=False, location=['json', 'form']),
put_parser.add_argument('password', type=str, required=False, location=['json', 'form'])
put_parser.add_argument('id_rol', type=int, required=False, location=['json', 'form']),

password_parser = reqparse.RequestParser()
password_parser.add_argument('new_password', type=str, required=True)
password_parser.add_argument('confirm_new_password', type=str, required=True)

class UsersResource(Resource):
    def get(self):
        try:
            users = User.query.all()

            if is_htmx_request():
                html = render_template('users/partials/table.html', users=users)
                return make_response(html, 200)

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
            if request.headers.get('Content-Type') == 'application/json':
                args = post_parser.parse_args()
            else:
                args = {
                    'username': request.form.get('username'),
                    'password': request.form.get('password'),
                    'confirm_password': request.form.get('confirm_password'),
                    'id_rol': request.form.get('id_rol')
                }
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
                if is_htmx_request():
                    errors_html = """
                        <div class="container">
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div>
                                <h3 class="font-bold">Errores de validación:</h3>
                                <ul class="list-disc pl-5">
                                    {}
                                </ul>
                            </div>
                        </div>                    
                    """.format("".join(f"<li>{ error }</li>" for error in errores))
                    return make_response(errors_html, 422)
                    
                else:
                    return {
                        'success': False,
                        'errors': errores,
                        'message': 'Hubo un problema al registrar el nuevo usuario'
                    }, 422

            nuevo_usuario = User(
                username=args['username'],
                password=args['password'],  # Se hashea automáticamente
                id_rol=args['id_rol']
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            if is_htmx_request():
                html = render_template('/components/alert.html', 
                                       success=True,
                                       message='¡Usuario creado exitosamente!',
                                       alert_type='alert-success')
                
                return make_response(html, 201)
            
            return {
                'success': True,
                'data': nuevo_usuario.to_dict(),
                'message': 'Usuario creado exitosamente'
            }, 201
        except Exception as e:
            db.session.rollback()

            if request.headers.get('HX-Request') == 'true':
                html = render_template('/components/alert.html',
                                       message=str(e),
                                       alert_type="alert-error")
                return make_response(html, 500)

            return {
                'success': False,
                'error': str(e),
                'message': 'Error al crear usuario'
            }, 500
        

class UserResource(Resource):
        def put(self, user_id):
            """ Actualizar usuario existente """
            try:
                if request.headers.get('Content-Type') == 'application/json':
                    args = put_parser.parse_args()
                else:
                    args = {
                    'username': request.form.get('username'),
                    'password': request.form.get('password'),
                    'confirm_password': request.form.get('confirm_password'),
                    'id_rol': request.form.get('id_rol')
                }
                usuario = User.query.get(user_id)
                errores = []
                if not usuario:
                    if is_htmx_request():
                        html = render_template('/components/alert.html',
                                               success=False,
                                               message='Usuario no encontrado',
                                               alert_type='alert-error')
                    return {
                        'success': False,
                        'message': 'Usuario no encontrado'
                    }, 404

                try:
                    validate_required(args['username'], 'Debe ingresar un nombre de usuario')
                    validate_length(args['username'], 'El nombre de usuario debe tener entre 2 y 100 caracteres', 2, 100)
                except ValueError as e:
                    errores.append(str(e))
                
                try:
                    validate_required(args['id_rol'], 'Debe ingresar un rol')
                    validate_numeric(args['id_rol'], 'Rol debe ser numerico')
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
                    if is_htmx_request():
                        errors_html = """
                            <div class="container">
                                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <div>
                                    <h3 class="font-bold">Errores de validación:</h3>
                                    <ul class="list-disc pl-5">
                                        {}
                                    </ul>
                                </div>
                            </div>                    
                        """.format("".join(f"<li>{ error }</li>" for error in errores))
                        return make_response(errors_html, 422)
                    return {
                        'success': False,
                        'errors': errores,
                        'message': 'Hubo un problema al editar la información del usuario'
                    }, 400


                if args['id_rol']:
                    usuario.id_rol = args['id_rol']

                db.session.commit()

                if is_htmx_request():
                    html = render_template('components/alert.html',
                                           success=True,
                                           message='Informacion de usuario actualizada exitosamente',
                                           alert_type='alert-success')
                    return make_response(html, 200)

                return {
                    'success': True,
                    'message': 'Información de usuario actualizado exitosamente',
                    'data': usuario.to_dict()
                }, 200

            except Exception as e:
                db.session.rollback()
                if is_htmx_request():
                    html = render_template('/components/alert.html',
                                           success=False,
                                           message=str(e),
                                           alert_type='alert-error')
                return {
                    'success': False,
                    'error': str(e),
                    'message': 'Error al actualizar la información de usuario'
                }, 500
            
        def delete(self, user_id):
            try:
                user = User.query.get(user_id)

                if not user:

                    if is_htmx_request():
                        html = render_template('/components/alert.html',
                                               success=False,
                                               message='No se encontro este usuario',
                                               alert_type='alert-error')
                        return make_response(html, 404)

                    return {
                        'success': False,
                        'message': 'No se encontró este usuario'
                    }, 404


                if user.soportes and len(user.soportes) > 0:
                    if is_htmx_request():
                        html = render_template('/components/alert.html',
                                               success=False, 
                                               message='Hay soportes vinculados a este usuario y no se puede borrar',
                                               alert_type='alert-error')
                        return make_response(html, 403)
                    
                    return {
                        'success': False,
                        'message': 'Hay soportes vinculados a este usuario y no se puede borrar'
                    }, 400

                db.session.delete(user)
                db.session.commit()

                if is_htmx_request():                  
                        html = render_template('/components/alert.html',
                            success=True,
                            message='¡Usuario eliminado exitosamente!',
                            alert_type='alert-success')
                        return make_response(html, 200)

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

    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        if is_htmx_request():
            html = render_template('users/partials/form_reiniciar_contraseña.html',
                                   user=user)
            return make_response(html, 200)

    def put(self, user_id):
        """ Reiniciar contraseña con confirmación """
        try:
            if request.headers.get('Content-Type') == 'application/json':
                args = password_parser.parse_args()
            else:
                args = {
                    'new_password': request.form.get('new_password'),
                    'confirm_new_password': request.form.get('confirm_new_password')
                }
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
                if is_htmx_request():
                    errors_html = """
                            <div class="container">
                                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <div>
                                    <h3 class="font-bold">Errores de validación:</h3>
                                    <ul class="list-disc pl-5">
                                        {}
                                    </ul>
                                </div>
                            </div>                    
                        """.format("".join(f"<li>{ error }</li>" for error in errores))
                    return make_response(errors_html, 422)

                return {
                    'success': False,
                    'errors': errores,
                    'message': 'Ha habido un problema reiniciando la clave'
                }, 422
            
            usuario.password = args['new_password']
            db.session.commit()

            if is_htmx_request():
                html = render_template('components/alert.html',
                                       success=True,
                                       message='Contraseña reiniciada exitosamente',
                                       alert_type='alert-success')
                return make_response(html, 200)
            return {
                'success': True,
                'message': 'Contraseña reiniciada exitosamente'
            }, 200
        except Exception as e:
            db.session.rollback()
            if is_htmx_request():
                html = render_template('components/alert.html',
                                       success=False,
                                       message=str(e),
                                       alert_type='alert-error')
                return make_response(html, 500)
            return {
                'success': True,
                'error': str(e),
                'message': 'Ha habido un problema reiniciando la clave'
            }, 500

class UserOptionResource(Resource):
    def get(self):
        users = User.query.all()

        if is_htmx_request():
            html = render_template('users/partials/users_options.html', users=users)
            return make_response(html, 200)             

class UserFormResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        roles = Rol.query.all()
        if is_htmx_request():
            html = render_template('users/partials/form_editar_usuario.html', user=user, roles=roles)
            return make_response(html, 200)
        return user.to_dict()