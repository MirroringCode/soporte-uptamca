from flask import Flask
from flask_restful import Api

app = Flask('Soporte-Uptamca')
api = Api(app)


@app.route('/')
def index():
    return '<h1>Hola mundo</h1>'

if __name__ == '__main__':
    app.run(debug=True)