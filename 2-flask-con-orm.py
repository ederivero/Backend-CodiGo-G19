from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, types
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.exceptions import ValidationError
# ORM una de las ventajas es que se usa para diferentes motores de base de datos por lo que si usamos uno en particular no podremos cambiar facilmente a otro motor de base de datos (postgre > mysql)
# from sqlalchemy.dialects.postgresql import 

app = Flask(__name__)
# se guardaran todas la configuraciones de nuestra aplicacion en Flask
# print(app.config)
# SQLALCHEMY cuando configuramos una base de datos que es postgres, utiliza el conector psycopg2 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@127.0.0.1:5432/colegio'
# busca la cadena de conexion a nuestra base de datos
conexion = SQLAlchemy(app) # configuracion hacia la base de datos

# Aca inicializamos las operaciones de migraciones 
Migrate(app,conexion)

# asi se declara un modelo (tabla)
class AlumnoModel(conexion.Model):
    # type_ > tipo de dato de esa columna
    id = Column(type_=types.Integer, autoincrement=True, primary_key=True, nullable=False)
    nombre = Column(type_=types.Text, nullable=False)
    correo = Column(type_=types.Text, nullable=False, unique=True)
    fechaNacimiento = Column(name='fecha_nacimiento', type_=types.TIMESTAMP)

    # para indicar como se deberia llamar la tabla en la base de datos
    __tablename__ = 'alumnos'


# Serializador > El que convierte tipos de datos complejos o instancias de clases a tipos de datos nativos (string, int)
class AlumnoSerializer(SQLAlchemyAutoSchema):
    class Meta:
        # Metadatos a la clase de la cual estamos haciendo la herencia es decir la clase SQLAlchemyAutoSchema
        # configuramos atributos para la herencia
        model = AlumnoModel
        # para que nos ayude a hacer la conversion de nuestros tipos de datos provenientes de la bd

@app.route('/')
def inicio():
    conexion.create_all() # crea todos los modelos que aun no existen en la base de datos, y si existen entonces los omite
    return {
        'message':'Bienvenido a mi API'
    }

@app.route('/crear-alumno', methods=['POST'])
def crearAlumno():
    data = request.get_json()
    serializador = AlumnoSerializer()

    # cargar de los datos primitivos a los datos necesarios para que funcione mi modelo y ademas hace la validacion correspondiente
    # si no es valida la informacion entonces LANZARA UN ERROR
    try:
        dataValidada = serializador.load(data)

        print(dataValidada)
        # inicializo mi nuevo registro del alumno
        nuevoAlumno =  AlumnoModel(**dataValidada)
        
        print(nuevoAlumno.id)

        # agregarlo a la base de datos
        conexion.session.add(nuevoAlumno)

        # guardarlo de manera permanente
        conexion.session.commit()
        print(nuevoAlumno.id)

        return {
            'message': 'Alumno registrado exitosamente'
        }, 201 # Created (Creacion)
    
    except ValidationError as errorValidacion:
        return {
            'message': 'Error al crear el alumno',
            'content': errorValidacion.args # donde se almacenaran los errores de la validacion
        }, 400 # Bad Request

@app.route('/listar-alumnos', methods = ['GET'])
def listarAlumnos():
    # SELECT * FROM alumnos;
    # query > cuando le pasamos la entidad podremos hacer busquedas, eliminaciones o actualizaciones con filtros, etc 
    alumnos = conexion.session.query(AlumnoModel).all()
    # Sin serializadores
    resultado = []
    for alumno in alumnos:
        resultado.append({
            'id': alumno.id,
            'nombre': alumno.nombre,
            'correo': alumno.correo,
            'fechaNacimiento': alumno.fechaNacimiento
        })


    # Con serializadores
    serializador = AlumnoSerializer()
    # si se le pasa mas de una instancia (una lista de instancias) entonces tenemos que indicarle mediante el parametro many
    resultado = serializador.dump(alumnos, many=True)
    return {
        'content':resultado
    }


@app.route('/devolver-alumno/<int:id>', methods=['GET'])
def devolverAlumno(id):
    # SELECT * FROM alumnos WHERE id = ... LIMIT 1;
    # https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#the-query-object
    alumnoEncontrado = conexion.session.query(AlumnoModel).where(AlumnoModel.id == id).first()

    if not alumnoEncontrado:
        return {
            'message': 'El alumno no existe'
        }, 404
    
    serializador = AlumnoSerializer()
    resultado = serializador.dump(alumnoEncontrado)

    return {
        'content': resultado
    }


if __name__ == '__main__':
    app.run(debug=True)