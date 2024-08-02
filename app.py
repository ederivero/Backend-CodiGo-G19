from flask import Flask
from instancias import conexion
from dotenv import load_dotenv
from os import environ
# busca el archivo .env y cargara las variables como si fueran variable de entorno
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= environ.get('DATABASE_URL')

# ahora aca le paso la configuracion de flask a SQLAlchemy
conexion.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)