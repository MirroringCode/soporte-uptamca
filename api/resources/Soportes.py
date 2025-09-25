from flask import render_template, make_response, request
from flask_restful import Resource, reqparse
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from models import Soporte, Personal, User, Departamento
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
put_parser.add_argument('fecha', type=str, required=False)

class SoportesResource(Resource):
    def get(self):
        try:
            soportes = Soporte.query.all()

            if 'text/html' in request.headers.get('Accept', '') or request.headers.get('HX-Request') == 'true':
                html = render_template('soportes/partials/table.html', soportes=soportes)
                return make_response(html, 200)

            return {
                'success': True,
                'data': [s.to_dict() for s in soportes],
                'count': len(soportes),
                'message': 'Lista de soportes obtenida exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error obteniendo la lista de soportes'
            }, 500

    def post(self):
        try:
            args = post_parser.parse_args()
            errores = []
            empleado = Personal.query.get(args['id_personal'])
            tecnico = User.query.get(args['atendido_por'])
            departamento = Departamento.query.get(args['id_departamento'])

            if not empleado and empleado != None:
                errores.append('No se ha encontrado a este empleado')
            if not tecnico and tecnico != None:
                errores.append('No se ha encontrado a este técnico')
            if not departamento and departamento != None:
                errores.append('No se ha encontrado el departamento')

            if errores:
                return {
                    'success': False,
                    'errors': errores,
                    'message': 'Ha habido un error registrando el soporte'
                }

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
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error creando el soporte'
            }, 500
    
class SoporteResource(Resource):
    def get(self, soporte_id):
        try:
            soporte = Soporte.query.get(soporte_id)
            if not soporte:
                return {
                    'success': False,
                    'message': 'No se ha encontrado el soporte especificado',
                }, 404
            return {
                'success': True,
                'data': soporte.to_dict(),
                'message': 'Información del soporte obtenida exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error al obtener información del soporte'
            }


    def put(self, soporte_id):
        try:
            args = put_parser.parse_args()
            soporte = Soporte.query.get(soporte_id)
            errores = []
            empleado = Personal.query.get(args['id_personal'])
            tecnico = User.query.get(args['atendido_por'])
            departamento = Departamento.query.get(args['id_departamento'])



            if not soporte:
                return {
                    'success': False,
                    'message': 'Soporte no encontrado'
                }, 404
            
            if not empleado:
                errores.append('No se ha encontrado a este empleado')
            if not tecnico:
                errores.append('No se ha encontrado a este técnico')
            if not departamento:
                errores.append('No se ha encontrado el departamento')

            if errores:
                return {
                    'success': False,
                    'errors': errores,
                    'message': 'Ha habido un error registrando el soporte'
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
            }, 200

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error actualizando la información del soporte'
            }, 500
        
    def delete(self, soporte_id):
        try:
            soporte = Soporte.query.filter(Soporte.id == soporte_id).first()
            if not soporte:
                return {
                    'success': False,
                    'message': 'Soporte no encontrado',
                }, 404
            
            db.session.delete(soporte)
            db.session.commit()
            return {
                'success': True,
                'message': 'soporte borrado exitosamente',
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Hubo un error al eliminar el soporte'
            }, 500



class SoporteStatusResource(Resource):
    def get(self):
        try:
            atendido_param = request.args.get('atendido')
            formato_param = request.args.get('formato')
            query = Soporte.query

            if atendido_param == 'si':
                query = query.filter(Soporte.atendido == True)
            elif atendido_param == 'no':
                query = query.filter(Soporte.atendido == False).order_by(desc(Soporte.fecha))
            
            soportes = query.all()

            if 'text/html' in request.headers.get('Accepts', '') or request.headers.get('HX-Request') == 'true':
                html = None
                if formato_param == 'card':
                    html = render_template('soportes/partials/soporte-reciente-card.html', soportes=soportes)
                if formato_param == 'table' or formato_param == None:
                    html = render_template('soportes/partials/table.html', soportes=soportes)
                return make_response(html, 200)

            return {
                'success': True,
                'data': [s.to_dict() for s in soportes] or 'No se encontraron soportes',
                'message': 'Soportes obtenidos exitosamente',
                'count': len(soportes),
            }, 200           
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error obteniendo los soportes atendidos'
            }, 500

class SoportesCountResource(Resource):
    def get(self):
        try:

            hoy = datetime.today()
            inicio_dia = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            inicio_mes = hoy.replace(day=1)

            diarios = Soporte.query.filter(
                Soporte.fecha >= inicio_dia
            ).count()

            semanales = Soporte.query.filter(
                Soporte.fecha >= inicio_semana
            ).count()

            mensuales = Soporte.query.filter(
                Soporte.fecha >= inicio_mes
            ).count()

            if 'text/html' in request.headers.get('Accepts', '') or request.headers.get('HX-Request') == 'true':
                html = render_template('soportes/partials/conteo.html', 
                                       diarios=diarios, 
                                       semanales=semanales, 
                                       mensuales=mensuales)
                return make_response(html, 200)

            return {
                'success': True,
                'data': {
                    'diarios': diarios,
                    'semanales': semanales,
                    'mensuales': mensuales
                },
                'message': 'Conteo obtenido exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'No se ha podido obtener el conteo'
            }


