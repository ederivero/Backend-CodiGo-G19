from models import UsuarioModel
from instancias import conexion
from flask_restful import Resource, request
from serializers import (RegistroSerializer,
                         LoginSerializer,
                         ActualizarUsuarioSerializer,
                         CambiarPasswordSerializer,
                         ResetearPasswordSerializer,
                         ConfirmarResetTokenSerializer)
from marshmallow.exceptions import ValidationError
from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utilitarios import enviarCorreo, encriptarTexto, desencriptarTexto
from json import loads, dumps


class RegistroController(Resource):
    def post(self):
        data = request.get_json()
        serializador = RegistroSerializer()
        try:
            dataValidada = serializador.load(data)
            print(dataValidada)
            # Proceso de hashing de la password
            salt = gensalt()  # un texto aleatorio que sera combinado con la contraseña para generar el hash de la misma
            password = dataValidada.get('password')
            # convertimos la password a bytes (tipo de dato)
            passwordBytes = bytes(password, 'utf-8')

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
                'message': 'Usuario creado exitosamente',
                'content': resultado
            }, 201

        except ValidationError as error:
            return {
                'message': 'Error al crear el usuario',
                'content': error.args
            }, 400

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
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(
                UsuarioModel.correo == dataSerializada.get('correo')).first()
            # si no existe retornar un mensaje que el usuario no existe
            if not usuarioEncontrado:
                return {
                    'message': 'El usuario no existe'
                }, 404
            print(usuarioEncontrado)
            password = usuarioEncontrado.password
            # convertimos la password de la bd a bytes
            passwordBytes = bytes(password, 'utf-8')
            passwordEntranteBytes = bytes(
                dataSerializada.get('password'), 'utf-8')
            validacionPassword = checkpw(passwordEntranteBytes, passwordBytes)

            # if not validacionPassword:
            if validacionPassword == False:
                return {
                    'message': 'Credenciales incorrectas'
                }, 400

            informacionAdicional = {
                'correo': usuarioEncontrado.correo
            }

            jwt = create_access_token(
                identity=usuarioEncontrado.id, additional_claims=informacionAdicional)

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

        usuarioEncontrado = conexion.session.query(UsuarioModel).where(
            UsuarioModel.id == identificador).first()
        serializador = RegistroSerializer()
        resultado = serializador.dump(usuarioEncontrado)

        return {
            'content': resultado
        }

    @jwt_required()
    def put(self):
        identificador = get_jwt_identity()

        usuarioEncontrado = conexion.session.query(UsuarioModel).where(
            UsuarioModel.id == identificador).first()
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
            }, 201

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
            dataValidada = serializador.load(data)
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(
                UsuarioModel.id == identificador).first()
            if not usuarioEncontrado:
                return {
                    'message': 'Usuario no existe'
                }, 404

            # Validar si la contraseña antigua es la contraseña del usuario, si no es retornar el mensaje ´Password antigua invalida´
            passwordAntigua = bytes(
                dataValidada.get('passwordAntigua'), 'utf-8')
            validarPassword = checkpw(passwordAntigua, bytes(
                usuarioEncontrado.password, 'utf-8'))

            if validarPassword == False:
                return {
                    'message': 'Las contraseña antigua es invalida'
                }, 400
            # si es la password entonces actualizarla pero antes hacer el hash de la misma y luego almacenarla
            nuevaPassword = bytes(dataValidada.get('passwordNueva'), 'utf-8')
            salt = gensalt()

            nuevaPasswordHash = hashpw(nuevaPassword, salt).decode('utf-8')
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


class ResetearPasswordController(Resource):
    def post(self):
        data = request.get_json()
        serializador = ResetearPasswordSerializer()
        try:
            dataSerializada = serializador.load(data)

            usuarioEncontrado = conexion.session.query(UsuarioModel).where(
                UsuarioModel.correo == dataSerializada.get('correo')).first()

            if not usuarioEncontrado:
                return {
                    'message': 'El usuario no existe en la base de datos'
                }, 400

            textoAEncriptar = {
                'correo': usuarioEncontrado.correo
            }

            # dumps en el modulo json lo que hace es convierte un diccionario a un string
            token = encriptarTexto(dumps(textoAEncriptar))
            url = f'http://localhost:5000/reset-password-frontend?token={
                token}'

            textoCorreo = """
Hola {},
Has solicitado el cambio de la contraseña de tu cuenta en Tienditapp, haz click en el siguiente <a href="{}">link</a> para proceder
<br>
<br>
Si no has sido tu omite este mensaje.
<br>
<br>
Gracias,
<br>
<br>
Atentamente.
<br>
<br>
El equipo mas chevere de todos
""".format(usuarioEncontrado.nombre, url)

            htmlCorreo = """
<html>
    <body>
        <p>Hola <b>{}</b>, <br>
            Has solicitado el cambio de la contraseña de tu cuenta en <b>Tienditapp</b>, si no has sido tu omite este mensaje.<br><br>
            Gracias,<br><br>
            Atentamente.<br><br>
            El equipo mas chevere de todos
        </p>
    </body>
</html>
"""

            # sirve para leer archivos del proyecto
            plantillaCorreo = open('plantilla_mensajeria.html', 'r')

            # lee todo el archivo y lo almacena en una variable
            textoPlantilla = plantillaCorreo.read()

            # ahora reemplazamos el texto del html por nuestro texto de nuestra variable
            textoResultado = textoPlantilla.replace(
                'cuerpo_correo', textoCorreo)

            enviarCorreo(usuarioEncontrado.correo,
                         'Has solicitado el cambio de tu contraseña', textoCorreo, textoResultado)

            return {
                'message': 'Reset completado exitosamente'
            }

        except ValidationError as error:
            return {
                'message': 'Error al resetear la password',
                'content': error.args
            }, 400


class ConfirmarResetTokenController(Resource):
    def post(self):
        data = request.get_json()
        serializador = ConfirmarResetTokenSerializer()
        try:
            dataValidada = serializador.load(data)
            # loads > convierte un string a diccionario siempre y cuando cumpla con el formato > '{"llave": "valor"}'
            informacion = loads(desencriptarTexto(dataValidada.get('token')))

            print(informacion)

            return {
                'message': ''
            }

        except ValidationError as error:
            return {
                'message': 'Error al hacer el request',
                'content': error.args
            }, 400
