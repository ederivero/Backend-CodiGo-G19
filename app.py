from flask import Flask
from instancias import conexion
from dotenv import load_dotenv
from os import environ
from models import *
from flask_migrate import Migrate
from controllers import *
# API > Application Program Interface
from flask_restful import Api 
from flask_jwt_extended import JWTManager
from datetime import timedelta

# busca el archivo .env y cargara las variables como si fueran variable de entorno
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET')
# cuanto va a durar la token de acceso , x defecto son 15min
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1, minutes=10, seconds=5)

# el JWTManage utiliza la aplicacion de Flask para leer las variables JWT_SECRET_KEY que esta sera la firma para la generacion de las token
JWTManager(app)
# Definimos la API de nuestra aplicacion de Flask
api = Api(app)


# ahora aca le paso la configuracion de flask a SQLAlchemy
conexion.init_app(app)

Migrate(app,conexion)

# Agregamos los recursos (controladores a nuestra API)
api.add_resource(CategoriasController, '/categorias')
api.add_resource(CategoriaController, '/categoria/<int:id>')
api.add_resource(ProductosController, '/productos')
api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController,'/login')
api.add_resource(PerfilController, '/perfil')

if __name__ == '__main__':
    app.run(debug=True)