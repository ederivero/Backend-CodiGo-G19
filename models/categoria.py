from instancias import conexion
from sqlalchemy import Column, types

class CategoriaModel(conexion.Model):
    id = Column(type_=types.Integer, primary_key=True, nullable=False, autoincrement=True)
    nombre = Column(type_=types.Text, nullable=False)
    fechaCreacion = Column(type_=types.TIMESTAMP, name='fecha_creacion')
    disponibilidad = Column(type_=types.Boolean, default=True)

    __tablename__ = 'categorias'