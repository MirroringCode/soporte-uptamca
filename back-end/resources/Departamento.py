from flask_restful import Resource
from models import Departamento

class DepartamentoResource(Resource):
    def get(self):
        try:
            departamentos = Departamento.query.all()
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

