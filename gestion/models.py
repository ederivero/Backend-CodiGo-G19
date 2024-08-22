from django.db import models
# Si queremos usar las columnas existentes en la tabla auth_user y agregar algunas otras columnas que necesitemos entonces usaremos la clase AbstractUser
# Si queremos eliminar todas las columnas y crear nuestro modelo auth_user a nuestro antojo entonces usaremos la clase AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_superuser(self, correo, nombre, apellido, password):
        # Este metodo es el que se llamara cuando queramos crear el usuario desde la terminal
        if not correo:
            raise ValueError('El usuario debe tener un correo')
        if not nombre:
            raise ValueError('El usuario debe tener un nombre')
        if not apellido:
            raise ValueError('El usuario debe tener un apellido')
        # normalize_email > quita los espacios al comienzo y al final y pone todo a minusculas para evitar errores
        correo_normalizado = self.normalize_email(correo)

        nuevo_usuario = self.model(
            correo=correo_normalizado, nombre=nombre, apellido=apellido)
        # set_password > genera el hash de la password usando bcrypt como en Flask y lo guarda en la columna password del modelo
        nuevo_usuario.set_password(password)

        # is_superuser > le da todos los permisos en el panel administrativo a este usuario
        nuevo_usuario.is_superuser = True
        nuevo_usuario.is_staff = True

        # creamos el nuevo usuario en la base de datos
        nuevo_usuario.save()


class Usuario(AbstractBaseUser):
    # Al crear un enum en la base de datos tenemos que indicar cuales son sus opciones con una lista de listas

    # La primera sera usada para guardar en la base de datos
    # mientras que la segunda sera para como lo mostrara al retornar la informacion de la base de datos
    # https://docs.djangoproject.com/en/5.1/ref/models/fields/#choices
    opcionesTipoUsuario = [['NOVIO', 'NOVIO'], [
        'INVITADO', 'INVITADO'], ['ADMIN', 'ADMIN']]

    opcionesTipoUsuario = {
        "NOVIO": "NOVIO",
        "INVITADO": "INVITADO",
        'ADMIN': 'ADMIN'
    }

    id = models.AutoField(primary_key=True)
    nombre = models.TextField(null=False)
    apellido = models.TextField(null=False)
    # EmailField > Crea una columna de tipo texto PERO al momento de crear el registro hace una validacion para sea un correo
    correo = models.EmailField(null=False, unique=True)
    numeroTelefonico = models.TextField(db_column='numero_telefonico')
    password = models.TextField(null=False)
    tipoUsuario = models.TextField(choices=opcionesTipoUsuario)

    # OPCIONALMENTE agregaremos las columnas para que funcione el panel administrativo
    # Sirve para ver si el usuario creado pertenece al equipo que puede acceder al panel administrativo porque tbn podemos tener usuarios que no 'trabajen' en la aplicacion, osea, clientes
    is_staff = models.BooleanField(default=False)

    # Sirve para ver si el usuario esta activo o no, aparte si no esta activo no podra ingresar al panel administrativo pero no implica que este sea o no un trabajador interno de la empresa
    is_active = models.BooleanField(default=True)
    # Puede darse el caso de que tengamos un trabajor que ya no trabaje (lo despidieron)

    # Para poder realizar el login en el panel administrativo hay que indicar que columna va a utilizar para poder realizar el login
    # esta columna debe de ser unica ya que al hacer el login podremos tener problemas si no lo es
    USERNAME_FIELD = 'correo'

    # Indicar que campos se tienen que solicitar al momento de crear un super usuario en la terminal
    # no va el USERNAME_FIELD y el password porque ya es implicito
    REQUIRED_FIELDS = ['nombre', 'apellido']

    # Como se va a comportar al momento de crear el usuario por la terminal / consola
    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'
