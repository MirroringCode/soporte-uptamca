from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from common import verify_db
from db import db
from datetime import timedelta


# Configuración de la App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/soportes-uptamca'
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False
app.config['JWT_SECRET_KEY'] = 'super1211'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True


jwt = JWTManager(app)
db.init_app(app)
api = Api(app)
CORS(app, expose_headers=['HX-Redirect'], supports_credentials=True)

from resources.Users import UsersResource, UserResource, PasswordResource, UserOptionResource, UserFormResource
from resources.Personal import PersonalResource, EmpleadoResource, PersonalOptionResource, FormEditarResource
from resources.Rol import RolResource
from resources.Departamento import DepartamentoResource
from resources.Soportes import SoportesResource, SoporteResource, SoporteStatusResource, SoportesCountResource, SoporteEditarFormResource
from resources.Auth import LoginResource, LogoutResource

# Estas son las rutas o URL de la api, con las que interactuará nuestro Front-end --- para thunder client
api.add_resource(UsersResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(PasswordResource, '/api/users/reset_password/<int:user_id>')
api.add_resource(UserOptionResource, '/api/users_options')
api.add_resource(UserFormResource, '/api/user_form/<int:user_id>')

api.add_resource(PersonalResource, '/api/personal')
api.add_resource(PersonalOptionResource, '/api/personal_options')
api.add_resource(EmpleadoResource, '/api/personal/<int:personal_id>')
api.add_resource(FormEditarResource, '/api/personal_form/<int:personal_id>')

api.add_resource(SoportesResource, '/api/soportes')
api.add_resource(SoporteResource, '/api/soportes/<int:soporte_id>')
api.add_resource(SoporteStatusResource, '/api/soporte_estatus')
api.add_resource(SoportesCountResource, '/api/soportes_count')
api.add_resource(SoporteEditarFormResource, '/api/soportes_form/<int:soporte_id>')

api.add_resource(RolResource, '/api/roles')
api.add_resource(DepartamentoResource, '/api/departamentos')

api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')

# Ejecuta la app
if __name__ == '__main__':
    app.run(debug=True)