from flask import request, make_response, render_template
from flask_restful import Resource
from models import Rol

class RolResource(Resource):
    def get(self):
        try:
            roles = Rol.query.all()

            if 'text/html' in request.headers.get('Accepts', '') or request.headers.get('HX-Request') == 'true':
                html = render_template('users/partials/rol_options.html', roles=roles)
                return make_response(html, 200)

            return {
                'success': True,
                'data': [r.to_dict() for r in roles],
                'count': len(roles),
                'Message': 'Lista de roles obtenida exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Hubo un error al obtener la lista de roles'
            }