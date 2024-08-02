from instancias import conexion
from sqlalchemy import Column, types
from enum import Enum

# Creamos un enumerable (Unicos valores a una columna)
class TipoUsuario(Enum):
    ADMIN = 'ADMIN'
    CLIENTE = 'CLIENTE'
    CAJERO = 'CAJERO'

class UsuarioModel(conexion.Model):
    id = Column(type_=types.Integer, autoincrement=True, primary_key=True)
    nombre = Column(type_=types.Text)
    correo = Column(type_=types.Text, unique=True, nullable=False)
    password = Column(type_=types.Text, nullable=False)
    tipoUsuario = Column(type_=types.Enum(TipoUsuario), nullable=False, default=TipoUsuario.CLIENTE, name='tipo_usuario')
    
    __tablename__= 'usuarios'