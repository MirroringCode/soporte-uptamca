from flask_restful import Resource
from flask import request, jsonify, make_response, render_template
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from models import User
from werkzeug.security import check_password_hash

class LoginResource(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.verify_password(password):
            html = render_template('/components/alert.html',
                                   success=False,
                                   message='No se encontro información que coincida con las credenciales dadas',
                                   alert_type='alert-error')
            return make_response(html, 401)
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'rol': user.id_rol})


        response = make_response("Login exitoso")
        response.headers['HX-Redirect'] = '/home.html'
        set_access_cookies(response, access_token)
        return response
    
class LogoutResource(Resource):
    def post(self):
        response = make_response('', 204)
        unset_jwt_cookies(response)
        response.headers['HX-Redirect'] = '/login.html'
        return response
