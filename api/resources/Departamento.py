from flask import request, render_template, make_response
from flask_restful import Resource
from models import Departamento
from common.check_htmx_request import is_htmx_request
from auth import jwt_required

class DepartamentoResource(Resource):
    @jwt_required
    def get(self):
        try:
            departamentos = Departamento.query.all()

            if is_htmx_request():
                html = render_template('personal/partials/departamentos_options.html', departamentos=departamentos)
                return make_response(html, 200)


            return {
                'success': True,
                'data': [d.to_dict() for d in departamentos],
                'message': 'Lista de departamentos obtenida exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Hubo un error al obtener los departamentos'
            }

