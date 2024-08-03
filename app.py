from flask import Flask
from instancias import conexion
from dotenv import load_dotenv
from os import environ
from models import *
from flask_migrate import Migrate
from controllers import *
# API > Application Program Interface
from flask_restful import Api 
# busca el archivo .env y cargara las variables como si fueran variable de entorno
load_dotenv()

app = Flask(__name__)

# Definimos la API de nuestra aplicacion de Flask
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI']= environ.get('DATABASE_URL')

# ahora aca le paso la configuracion de flask a SQLAlchemy
conexion.init_app(app)

Migrate(app,conexion)

# Agregamos los recursos (controladores a nuestra API)
api.add_resource(CategoriasController, '/categorias')
api.add_resource(CategoriaController, '/categoria/<int:id>')
api.add_resource(ProductosController, '/productos')

if __name__ == '__main__':
    app.run(debug=True)