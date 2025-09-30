from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from common import verify_db
from db import db


# Configuración de la App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/soportes-uptamca'
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False


db.init_app(app)
api = Api(app)
CORS(app)

from resources.Users import UsersResource, UserResource, PasswordResource, UserOptionResource, UserFormResource
from resources.Personal import PersonalResource, EmpleadoResource, PersonalOptionResource
from resources.Rol import RolResource
from resources.Departamento import DepartamentoResource
from resources.Soportes import SoportesResource, SoporteResource, SoporteStatusResource, SoportesCountResource

# Estas son las rutas o URL de la api, con las que interactuará nuestro Front-end --- para thunder client
api.add_resource(UsersResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(PasswordResource, '/api/users/reset_password/<int:user_id>')
api.add_resource(UserOptionResource, '/api/users_options')
api.add_resource(UserFormResource, '/api/user_form/<int:user_id>')

api.add_resource(PersonalResource, '/api/personal')
api.add_resource(PersonalOptionResource, '/api/personal_options')
api.add_resource(EmpleadoResource, '/api/personal/<int:personal_id>')

api.add_resource(SoportesResource, '/api/soportes')
api.add_resource(SoporteResource, '/api/soportes/<int:soporte_id>')
api.add_resource(SoporteStatusResource, '/api/soporte_estatus')
api.add_resource(SoportesCountResource, '/api/soportes_count')

api.add_resource(RolResource, '/api/roles')
api.add_resource(DepartamentoResource, '/api/departamentos')

# Ejecuta la app
if __name__ == '__main__':
    app.run(debug=True)