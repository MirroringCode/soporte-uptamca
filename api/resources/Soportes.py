from flask import render_template, make_response, request
from flask_restful import Resource, reqparse
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from models import Soporte, Personal, User, Departamento
from db import db
from common.validator import (
    validate_required,
    validate_length,
    validate_numeric,
    validate_date_format
)
from common.check_htmx_request import is_htmx_request
from auth import jwt_required

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
    @jwt_required
    def get(self):
        try:
            soportes = Soporte.query.all()
            if is_htmx_request():
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
        # PENDIENTE, hacer que atendido cuando sea 0 cuente como false  y validar atendido_por solo cuando está en el request 
        try:
            if request.headers.get('Content-Type') == 'application/json':
                args = post_parser.parse_args()
            else:
                args = {
                    'motivo': request.form.get('motivo'),
                    'atendido': request.form.get('atendido') == '1',
                    'atendido_por': request.form.get('atendido_por'),
                    'id_personal': request.form.get('id_personal'),
                    'id_departamento': request.form.get('id_departamento'),
                    'fecha': request.form.get('fecha')
                }
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

            try:
                validate_required(args['motivo'], 'Debe indicar el motivo')
                validate_length(args['motivo'], 'el motivo debe contener entre 3 y 100 caracteres', min_length=3, max_length=100)
            except ValueError as e:
                errores.append(str(e))

            if args.get('atendido_por'):
                try:
                    validate_numeric(args['atendido_por'], 'Solo valores numericos en la id del técnico')
                except ValueError as e:
                    errores.append(str(e))

            try:
                validate_required(args['id_personal'], 'Debe indicar al personal solicitante')
                validate_numeric(args['id_personal'], 'Solo valores numericos en la id del empleado solicitante')
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['id_departamento'], 'Debe indicar que departamento solicitó este soporte')
                validate_numeric(args['id_departamento'], 'Solo valores numericos en la id del departamento')
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['fecha'], 'Debe indicar la fecha del soporte')
            except ValueError as e:
                errores.append(str(e))

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
                    'message': 'Ha habido un error registrando el soporte'
                }, 422

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

            if is_htmx_request():
                html = render_template('/components/alert.html',
                                       success=True,
                                       message='¡Alerta creada exitosamente!',
                                       alert_type='alert-success')
                return make_response(html, 201)
            return {
                'success': True,
                'message': 'Soporte creado exitosamente'
            }, 201
        except Exception as e:
            db.session.rollback()

            if is_htmx_request():
                html = render_template('/components/alert.html',
                                       success=False,
                                       message=str(e),
                                       alert_type='alert-error')
                return make_response(html, 500)
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error creando el soporte'
            }, 500
    
class SoporteResource(Resource):
    @jwt_required
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
            if request.headers.get('Content-Type') == 'application/json':
                args = put_parser.parse_args()
            else:
                args = {
                    'motivo': request.form.get('motivo'),
                    'atendido': request.form.get('atendido') == '1',
                    'atendido_por': request.form.get('atendido_por'),
                    'id_personal': request.form.get('id_personal'),
                    'id_departamento': request.form.get('id_departamento'),
                    'fecha': request.form.get('fecha')
                }

            soporte = Soporte.query.get(soporte_id)
            errores = []
            empleado = Personal.query.get(args['id_personal'])
            tecnico = User.query.get(args['atendido_por'])
            departamento = Departamento.query.get(args['id_departamento'])



            if not soporte:
                if is_htmx_request():
                    html = render_template('/components/alert.html',
                                           Success=False,
                                           message='Usuario no encontrado',
                                           alert_type='alert-error')
                    return make_response(html, 404)
                return {
                    'success': False,
                    'message': 'Soporte no encontrado'
                }, 404
            
            if not empleado and empleado != None:
                errores.append('No se ha encontrado a este empleado')
            if not tecnico and tecnico != None:
                errores.append('No se ha encontrado a este técnico')
            if not departamento and departamento != None:
                errores.append('No se ha encontrado el departamento')

            try:
                validate_required(args['motivo'], 'Debe indicar el motivo')
                validate_length(args['motivo'], 'el motivo debe contener entre 3 y 100 caracteres', min_length=3, max_length=100)
            except ValueError as e:
                errores.append(str(e))

            if args.get('atendido_por'):
                try:
                    validate_numeric(args['atendido_por'], 'Solo valores numericos en la id del técnico')
                except ValueError as e:
                    errores.append(str(e))

            try:
                validate_required(args['id_personal'], 'Debe indicar al personal solicitante')
                validate_numeric(args['id_personal'], 'Solo valores numericos en la id del empleado solicitante')
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['id_departamento'], 'Debe indicar que departamento solicitó este soporte')
                validate_numeric(args['id_departamento'], 'Solo valores numericos en la id del departamento')
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['fecha'], 'Debe indicar la fecha del soporte')
            except ValueError as e:
                errores.append(str(e))

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
                    'message': 'Ha habido un error registrando el soporte'
                }

            if args['motivo']:
                soporte.motivo = args['motivo']
            if args['atendido'] != None:
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

            if is_htmx_request():
                html = render_template('/components/alert.html',
                                       success=True,
                                       message='Soporte modificado exitosamente',
                                       alert_type='alert-success')
                return make_response(html, 200)
            return {
                'success': True,
                'message': 'Soporte actualizado exitosamente',
                'data': soporte.to_dict()
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
                'message': 'Ha habido un error actualizando la información del soporte'
            }, 500
        
    def delete(self, soporte_id):
        try:
            soporte = Soporte.query.filter(Soporte.id == soporte_id).first()
            if not soporte:
                if is_htmx_request():
                    html = render_template('/components/alert.html', 
                                           success=False,
                                           message='No se encontró este soporte',
                                           alert_type='alert-error')
                    return make_response(html, 404)
                return {
                    'success': False,
                    'message': 'Soporte no encontrado',
                }, 404
            
            db.session.delete(soporte)
            db.session.commit()
            if is_htmx_request():
                    html = render_template('/components/alert.html', 
                                           success=True,
                                           message='¡Soporte eliminado exitosamente!',
                                           alert_type='alert-success')
                    return make_response(html, 200)
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
    @jwt_required
    def get(self):
        try:
            atendido_param = request.args.get('atendido')
            formato_param = request.args.get('formato')
            alerta_param = request.args.get('es_alerta')
            query = Soporte.query

            if atendido_param == 'si':
                query = query.filter(Soporte.atendido == True)
            elif atendido_param == 'no':
                query = query.filter(Soporte.atendido == False).order_by(desc(Soporte.fecha))
            
            soportes = query.all()

            if is_htmx_request():
                html = None
                if formato_param == 'card':
                    html = render_template('soportes/partials/soporte-reciente-card.html', soportes=soportes)
                if formato_param == 'table' or formato_param == None:
                    if alerta_param == 'si':
                        html = render_template('soportes/partials/table.html', 
                                               soportes=soportes,
                                               es_alerta=True)
                    else:
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
    @jwt_required
    def get(self):
        try:

            # hoy = datetime.today()
            # inicio_dia = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
            # inicio_semana = hoy - timedelta(days=hoy.weekday())
            # inicio_mes = hoy.replace(day=1)

            atendidos = Soporte.query.filter(
                Soporte.atendido == 1
            ).count()

            no_atendidos = Soporte.query.filter(
                Soporte.atendido == 0
            ).count()

            total = Soporte.query.count()

            if is_htmx_request():
                html = render_template('soportes/partials/conteo.html', 
                                       atendidos=atendidos, 
                                       no_atendidos=no_atendidos, 
                                       total=total)
                return make_response(html, 200)

            return {
                'success': True,
                'data': {
                    'atendidos': atendidos,
                    'no_atendidos': no_atendidos,
                    'total': total
                },
                'message': 'Conteo obtenido exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'No se ha podido obtener el conteo'
            }

class SoporteEditarFormResource(Resource):
    @jwt_required
    def get(self, soporte_id):
        soporte = Soporte.query.get_or_404(soporte_id)
        departamentos = Departamento.query.all()
        empleados = Personal.query.all()
        users = User.query.all()

        tipo_editar_param = request.args.get('tipo_editar')

        if tipo_editar_param == 'alerta':
            html = render_template('soportes/partials/form_editar_alerta.html',
                                   soporte=soporte,
                                   empleados=empleados,
                                   departamentos=departamentos,
                                   users=users)
            return make_response(html, 200)
        elif tipo_editar_param == 'soporte':
            html = render_template('soportes/partials/form_editar_soporte.html',
                                   soporte=soporte,
                                   empleados=empleados,
                                   departamentos=departamentos,
                                   users=users)
            return make_response(html, 200)
