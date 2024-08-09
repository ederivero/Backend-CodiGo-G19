from models import UsuarioModel
from instancias import conexion
from flask_restful import Resource, request
from serializers import (RegistroSerializer, 
                         LoginSerializer, 
                         ActualizarUsuarioSerializer,
                         CambiarPasswordSerializer)
from marshmallow.exceptions import ValidationError
from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
            password = usuarioEncontrado.password
            # convertimos la password de la bd a bytes
            passwordBytes = bytes(password,'utf-8')
            passwordEntranteBytes = bytes(dataSerializada.get('password'), 'utf-8')
            validacionPassword = checkpw(passwordEntranteBytes, passwordBytes)

            # if not validacionPassword:
            if validacionPassword == False:
                return {
                    'message': 'Credenciales incorrectas'
                }, 400
            
            informacionAdicional = {
                'correo': usuarioEncontrado.correo
            }

            jwt = create_access_token(identity= usuarioEncontrado.id, additional_claims= informacionAdicional)

            return {
                'message': 'Bienvenido',
                'content': jwt
            }
        
        except ValidationError as error:
            return {
                'message': 'Error al hacer el login',
                'content': error.args
            }
        
class PerfilController(Resource):
    # indica que ahora este metodo le tenemos que pasar de manera obligatoria la token y este metodo validara que la token sea correcta y que tenga tiempo de vida y sino no podremos ingresar al metodo
    @jwt_required()
    def get(self):
        # devuelve el identificador de la token (id del usuario)
        identificador = get_jwt_identity()
        print(identificador)
        
        usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.id == identificador).first()
        serializador = RegistroSerializer()
        resultado = serializador.dump(usuarioEncontrado)

        return {
            'content': resultado
        }
    
    @jwt_required()
    def put(self):
        identificador = get_jwt_identity()

        usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.id == identificador).first()
        data = request.get_json()

        if not usuarioEncontrado:
            return {
                'message': 'El usuario no se encuentra en la base de datos'
            }, 400

        try:
            serializador = ActualizarUsuarioSerializer()
            dataValidada = serializador.load(data)
            
            # Si queremos actualizar un campo o varios campos basta con modificalos en la instancia y luego guardarlo en la bd
            usuarioEncontrado.nombre = dataValidada.get('nombre')
            
            conexion.session.commit()
            serializadorUsuario = RegistroSerializer()
            resultado = serializadorUsuario.dump(usuarioEncontrado)

            return {
                'message': 'Usuario actualizado exitosamente',
                'content': resultado
            },201

        except ValidationError as error:
            return {
                'message': 'Error al actualizar el usuario',
                'content': error.args
            }, 400


class CambiarPasswordController(Resource):
    @jwt_required()
    def put(self):
        data = request.get_json()
        identificador = get_jwt_identity()
        serializador = CambiarPasswordSerializer()
        try:
            dataValidada =serializador.load(data)
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.id == identificador).first()
            if not usuarioEncontrado:
                return {
                    'message': 'Usuario no existe'
                }, 404
            
            # Validar si la contraseña antigua es la contraseña del usuario, si no es retornar el mensaje ´Password antigua invalida´
            passwordAntigua = bytes(dataValidada.get('passwordAntigua'),'utf-8')
            validarPassword = checkpw(passwordAntigua,bytes(usuarioEncontrado.password,'utf-8'))

            if validarPassword == False:
                return {
                    'message': 'Las contraseña antigua es invalida'
                }, 400
            # si es la password entonces actualizarla pero antes hacer el hash de la misma y luego almacenarla
            nuevaPassword = bytes(dataValidada.get('passwordNueva'), 'utf-8')
            salt = gensalt()

            nuevaPasswordHash = hashpw(nuevaPassword,salt).decode('utf-8')
            # si se logra actualiza la password retornar un mensaje de exito 
            usuarioEncontrado.password = nuevaPasswordHash
            conexion.session.commit()

            return {
                'message': 'Password actualizada exitosamente'
            }
            
        except ValidationError as error:
            return {
                'message': 'Error al cambiar la password',
                'content': error.args
            }, 400
