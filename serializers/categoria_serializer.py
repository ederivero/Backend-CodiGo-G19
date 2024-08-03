from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import CategoriaModel
from marshmallow import Schema, fields

class CategoriaSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = CategoriaModel


# Si no quisieramos utilizar nuestro marshmallow-sqlalchemy 
# y hacer el serializador manualmente
class ManualCategoriaSerializer(Schema):
    # si vamos a utilizar un atributo que solamente va a ser para mostrar la informacion
    id = fields.Integer(dump_only=True)
    # load_only > solamente se usara para cuando querramos devolver la informacion pero no para leerla 
    nombre = fields.String(required=True)
    fechaCreacion = fields.DateTime(format='iso')
    disponibilidad = fields.Boolean()