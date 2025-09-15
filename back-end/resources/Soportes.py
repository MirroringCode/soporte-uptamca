from flask_restful import Resource, reqparse
from models import Soporte
from db import db

post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('motivo', type=str, required=True, help='Debe indicar el motivo del soporte')
post_parser.add_argument('atendido', type=bool, required=False, help="El soporte fue atendido o no")
post_parser.add_argument('atendido_por', type=int, required=False, help="Técnico que atendió el soporte")
post_parser.add_argument('id_personal', type=int, required=False, help='Empleado que solicitó el soporte')
post_parser.add_argument('id_departamento', type=int, required=True, help='Debe indicar desde que departamento se solicitó el soporte')
post_parser.add_argument('fecha', type=str, required=True, help="Debe indicar la fecha del soporte")

put_parser = reqparse.RequestParser(bundle_errors=False)
put_parser.add_argument('motivo', type=str, required=False)
put_parser.add_argument('atendido', type=bool, required=False)
put_parser.add_argument('atendido_por', type=int, required=False)
put_parser.add_argument('id_personal', type=int, required=False)
put_parser.add_argument('id_departamento', type=int, required=False)
put_parser.add_argument('fecha', type=str, required=True)

""" PENDIENTE POR HACER:
- Método PUT
- Validaciones personalizadas para PUT y POST
- Lógica de soportes atendidos (marcar como atendido, ver los soportes atendidos...)
- FILTRADOS de soportes (ya sea por quien lo atendio, departamento, si está atendido, etc)
 """

class SoportesResource(Resource):
    def get(self):
        try:
            soportes = Soporte.query.all()
            return {
                'success': True,
                'data': [s.to_dict() for s in soportes],
                'count': len(soportes),
                'message': 'Lista de soportes obtenida exitosamente'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error obteniendo la lista de soportes'
            }

    def post(self):
        try:
            args = post_parser.parse_args()
            nuevo_soporte = Soporte(
                motivo=args['motivo'],
                atendido=args['atendido'] if 'atendido' in args else False,
                atendido_por=args['atendido_por'],
                id_personal=args['id_personal'],
                id_departamento=args['id_departamento'],
                fecha=args['fecha']
            )

            db.session.add(nuevo_soporte)
            db.session.commit()

            return {
                'success': True,
                'message': 'Soporte creado exitosamente'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error creando el soporte'
            }
    
class SoporteResource(Resource):
    def put(self, soporte_id):
        try:
            args = put_parser.parse_args()
            soporte = Soporte.query.get(soporte_id)

            if not soporte:
                return {
                    'success': False,
                    'message': 'Soporte no encontrado'
                }
            if args['motivo']:
                soporte.motivo = args['motivo']
            if 'atendido' in args:
                soporte.atendido = args['atendido']
            if args['atendido_por']:
                soporte.atendido_por = args['atendido_por']
            if args['id_personal']:
                soporte.id_personal = args['id_personal']
            if args['id_departamento']:
                soporte.id_departamento = args['id_departamento']
            if args['fecha']:
                soporte.fecha = args['fecha']
            db.session.commit()
            return {
                'success': True,
                'message': 'Soporte actualizado exitosamente',
                'data': soporte.to_dict()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error actualizando la información del soporte'
            }


class SoporteAtendidoResource(Resource):
    def get(self):
        return {
            'message': 'Soportes atendidos'
        }