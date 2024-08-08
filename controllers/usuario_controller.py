from models import UsuarioModel
from instancias import conexion
from flask_restful import Resource, request
from serializers import RegistroSerializer, LoginSerializer
from marshmallow.exceptions import ValidationError
from bcrypt import gensalt, hashpw
from sqlalchemy.exc import IntegrityError

class RegistroController(Resource):
    def post(self):
        data = request.get_json()
        serializador = RegistroSerializer()
        try:
            dataValidada = serializador.load(data)
            print(dataValidada)
            # Proceso de hashing de la password
            salt = gensalt() # un texto aleatorio que sera combinado con la contraseña para generar el hash de la misma
            password = dataValidada.get('password')
            # convertimos la password a bytes (tipo de dato)
            passwordBytes = bytes(password,'utf-8')
            
            # generara el hash de nuestra password
            hash = hashpw(passwordBytes, salt)
            # decode > convierte los bytes a texto
            hashString = hash.decode('utf-8')

            # ahora modificamos el valor de la password por el hash generado
            dataValidada['password'] = hashString

            nuevoUsuario = UsuarioModel(**dataValidada)

            conexion.session.add(nuevoUsuario)
            conexion.session.commit()

            resultado = serializador.dump(nuevoUsuario)

            print(hashString)
            return {
                'message':'Usuario creado exitosamente',
                'content': resultado
            }, 201
        
        except ValidationError as error:
            return {
                'message':'Error al crear el usuario',
                'content': error.args
            },400
        
        except IntegrityError as error:
            # Esta es la excepcion cuando el correo en la bd ya exista
            return {
                'message': 'Error al crear el usuario',
                'content': 'El usuario con correo {} ya existe'.format(data.get('correo'))
            }


class LoginController(Resource):
    def post(self):
        data = request.get_json()
        serializador = LoginSerializer()
        try:
            dataSerializada = serializador.load(data)
            print(dataSerializada)
            # Busquen el usuario en la base de datos
            # SELECT * FROM usuarios WHERE correo = '....' LIMIT 1;
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.correo == dataSerializada.get('correo')).first()
            # si no existe retornar un mensaje que el usuario no existe
            if not usuarioEncontrado:
                return {
                    'message':'El usuario no existe'
                }, 404
            print(usuarioEncontrado)
            return {
                'message': 'Bienvenido'
            }
        
        except ValidationError as error:
            return {
                'message': 'Error al hacer el login',
                'content': error.args
            }