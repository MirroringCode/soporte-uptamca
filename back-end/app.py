from flask import Flask
from flask_restful import Api
from common import verify_db
from db import db


# Configuración de la App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/soportes-uptamca'
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False


db.init_app(app)
api = Api(app)

from resources.Users import UsersResource
from resources.Personal import PersonalResource
from resources.Rol import RolResource
from resources.Departamento import DepartamentoResource

# Estas son las rutas o URL de la api, con las que interactuará nuestro Front-end
api.add_resource(UsersResource, '/api/users/')
api.add_resource(PersonalResource, '/api/personal')
api.add_resource(RolResource, '/api/roles')
api.add_resource(DepartamentoResource, '/api/departamentos')

# Ejecuta la app
if __name__ == '__main__':
    app.run(debug=True)