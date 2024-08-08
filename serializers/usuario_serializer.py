from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
# https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html
from marshmallow import validate # funciones que me ayudaran con validaciones adicionales
from models import UsuarioModel, TipoUsuario
from marshmallow_enum import EnumField
from marshmallow import Schema, fields

class RegistroSerializer(SQLAlchemyAutoSchema):
    # Las columnas que usan Enum marshmallow_sqlalchemy no sabe como convertirlas cuando son deserializadas entonces se usa la clase EnumField para ayudarles con ese proceso
    tipoUsuario = EnumField(TipoUsuario)

    # xxxxx@xxxxx.xxx
    # aparte de las validaciones que nos brinda marshmallow_sqlalchemy le estamos agregando validar que sea un correo
    correo = auto_field(validate=validate.Email(error='El correo no cumple con el formato correcto'))
    # load_only > solo se usara este field para la serializacion mas no para la deserializacion
    # dump_only > solo se usara para la deserializacion mas no para la serializacion
    password = auto_field(load_only=True)

    class Meta:
        model = UsuarioModel


# Este es un serializador creado desde 0 sin modelos
class LoginSerializer(Schema):
    correo = fields.Email(required=True)
    password = fields.String(required=True)