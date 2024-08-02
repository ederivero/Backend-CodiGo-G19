from flask_sqlalchemy import SQLAlchemy


# Creamos la unica instancia de nuestra clase SQLAlchemy que sera la encargada de hacer todas las peticiones a la base de datos
conexion = SQLAlchemy()