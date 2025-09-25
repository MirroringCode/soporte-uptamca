from flask import request, render_template, make_response
from flask_restful import Resource
from models import Departamento

class DepartamentoResource(Resource):
    def get(self):
        try:
            departamentos = Departamento.query.all()

            if 'text/html' in request.headers.get('Accepts', '') or request.headers.get('HX-Request') == 'true':
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

