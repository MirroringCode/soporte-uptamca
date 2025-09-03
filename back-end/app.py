from flask import Flask
from flask_restful import Api
from common import verify_db
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/soportes-uptamca'
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False

db.init_app(app)
api = Api(app)


from resources.Users import UsersResource

api.add_resource(UsersResource, '/api/users/')

if __name__ == '__main__':
    app.run(debug=True)