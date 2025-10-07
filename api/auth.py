from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from flask import jsonify, request, make_response, render_template
from models import User
from common.check_htmx_request import is_htmx_request

def jwt_required(fn):
    @wraps(fn)

    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            if is_htmx_request():
                response = make_response('', 401)
                response.headers['HX-Redirect'] = '/login.html'
                return response
            else:
                return jsonify({'success': False, 'message': 'No autorizado'}), 401
        
    return wrapper

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_rol = claims.get('rol')
            if user_rol not in roles:
                if is_htmx_request():
                    response = make_response('', 403)
                    response.headers['HX-Redirect'] = '/home.html'
                    return response
                return jsonify({
                    'success': False,
                    'message': 'No autorizado'
                    }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
