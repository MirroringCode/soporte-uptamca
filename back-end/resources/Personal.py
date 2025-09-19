from flask_restful import Resource, reqparse
from models import Personal, Departamento
from common.validator import (
    validate_length,
    validate_required,
    validate_numeric,
    validate_regex
)
from db import db


post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('cedula', type=str, required=True, help='Debe indicar la cédula del empleado', location='json')
post_parser.add_argument('nombre', type=str, required=True, help='Debe indicar el nombre del empleado', location='json') 
post_parser.add_argument('apellido', type=str, required=True, help='Debe indicar el apellido del empleado', location='json')
post_parser.add_argument('id_departamento', type=int, required=True, help='Debe indicar a que departamento pertenece el empleado', location='json')

put_parser = reqparse.RequestParser(bundle_errors=True)
put_parser.add_argument('cedula', type=str, required=False, help='Debe indicar la cédula del empleado', location='json')
put_parser.add_argument('nombre', type=str, required=False, help='Debe indicar el nombre del empleado', location='json') 
put_parser.add_argument('apellido', type=str, required=False, help='Debe indicar el apellido del empleado', location='json')
put_parser.add_argument('id_departamento', type=int, required=False, help='Debe indicar a que departamento pertenece el empleado', location='json') 

""" PENDIENTE POR HACER
- """

class PersonalResource(Resource):
    """ Método para traer todos los empleados existentes en base de datos """
    def get(self):
        try:
            # Hace consulta a la base de datos
            empleados = Personal.query.all()

            # Si todo sale bien devuelve respuesta en formato JSON
            return {
                'success': True,
                'data': [e.to_dict() for e in empleados],
                'count': len(empleados),
                'message': 'Lista de empleados obtenida exitosamente'
            }, 200
        except Exception as e:
            # Si ocurre un error, envía respuesta en formato JSON en conjunto con el error
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error obteniendo la lista de empleados' 
            }, 500

    """ Método para crear un nuevo empleado """
    def post(self):
        try:
            args = post_parser.parse_args()
            errores = []
            if Personal.query.filter_by(cedula=args['cedula']).first():
                errores.append('Ya existe un empleado con esa cédula')

            departamento = Departamento.query.get(args['id_departamento'])
            if not departamento:
                errores.append('El departamento especificado no existe') 
            
            try:
                validate_required(args['cedula'])
                validate_numeric(args['cedula'])
                validate_length(args['cedula'], 8, 10)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['nombre'])
                validate_length(args['nombre'], 4, 100)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['apellido'])
                validate_length(args['apellido'], 4, 100)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['id_departamento'])
                validate_numeric(args['id_departamento'])
            except ValueError as e:
                errores.append(str(e)) 

            if errores:
                return {
                    'success': False,
                    'errors': errores,
                    'message':'Ha habido un problema registrando al nuevo empleado'
                }

            nuevo_empleado = Personal(
                cedula=args['cedula'],
                nombre=args['nombre'],
                apellido=args['apellido'],
                id_departamento=args['id_departamento']
            )
            
            db.session.add(nuevo_empleado)
            db.session.commit()

            return {
                'success': True,
                'message': 'Empleado creado exitosamente',
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error creando el empleado'
            }, 500
            

class EmpleadoResource(Resource):
    def put(self, personal_id):
        try:
            args = put_parser.parse_args()
            empleado = Personal.query.get(personal_id)
            errores = []
            if not empleado:
                return {
                    'success': False,
                    'message': 'Empleado no encontrado'
                }, 404
            
            if args['cedula'] and args['cedula'] != empleado.cedula:
                if Personal.query.filter_by(cedula=args['cedula']).filter(Personal.id != personal_id).first():
                    errores.append('Ya existen un empleado con esa cédula')
                empleado.cedula = args['cedula']

            departamento = Departamento.query.get(args['id_departamento'])
            if not departamento:
                errores.append('El departamento especificado no existe') 

            try:
                validate_required(args['cedula'])
                validate_numeric(args['cedula'])
                validate_length(args['cedula'], 8, 10)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['nombre'])
                validate_length(args['nombre'], 4, 100)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['apellido'])
                validate_length(args['apellido'], 4, 100)
            except ValueError as e:
                errores.append(str(e))

            try:
                validate_required(args['id_departamento'])
                validate_numeric(args['id_departamento'])
            except ValueError as e:
                errores.append(str(e))

            if errores:
                return {
                    'success': False,
                    'errors': errores,
                    'message': 'Ha habido un error modificando la información del empleado'
                }

            if args['nombre']:
                empleado.nombre = args['nombre']
            if args['apellido']:
                empleado.apellido = args['apellido']
            if args['id_departamento']:
                empleado.id_departamento = args['id_departamento']
            
            db.session.commit()
            return {
                'success': True,
                'message': f'Información de empleado actualizada exitosamente',
                'data': empleado.to_dict()
            }, 200
        
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Ha habido un error actualizando la información del empleado'
            }, 500
    
    def delete(self, personal_id):
        try:
            empleado = Personal.query.get(personal_id)
            if not empleado:
                return {
                    'success': False,
                    'message': 'Empleado no encontrado'
                }, 404
            
            if empleado.soportes_solicitados and len(empleado.soportes_solicitados) > 0:
                return {
                    'success': False,
                    'message': 'Hay soportes solicitados vinculados a este empleado y no se puede borrar'
                }, 400

            db.session.delete(empleado)
            db.session.commit()
            return {
                'success': True,
                'message': 'Información del empleado eliminada exitosamente'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'No se ha podido eliminar información del empleado'
            }, 500
         
    