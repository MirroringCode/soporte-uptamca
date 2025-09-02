from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from common import verify_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/soportes-uptamca'
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False

db = SQLAlchemy(app)
api = Api(app)



if __name__ == '__main__':
    with app.app_context():
        if(verify_db.verificarSetupDB(db)):
            print('Iniciando server flask')
            app.run(debug=True)
        else:
            print("hubo un error con la base de datos")