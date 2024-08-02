from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, types
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql.expression import and_

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

@app.route('/actualizar-alumno/<int:id>', methods =['PUT'])
def actualizarAlumno(id):
    # SELECT id FROM alumnos WHERE id = ....
    alumnoEncontrado = conexion.session.query(AlumnoModel).with_entities(AlumnoModel.id).where(AlumnoModel.id == id).first()
    print(alumnoEncontrado)
    if not alumnoEncontrado:
        return {
            'message': 'El alumno no existe'
        }, 404
    
    serializador = AlumnoSerializer()
    try:
        dataValidada = serializador.load(request.get_json())
        # en el metodo update se tiene que pasar el diccionario con los valores a actualizar
        # UPDATE alumnos SET .... WHERE id = ...;
        conexion.session.query(AlumnoModel).where(AlumnoModel.id == id).update(dataValidada)
        conexion.session.commit()

        # Ahora procedemos a buscar el alumno actualizado para devolverlo
        resultado = conexion.session.query(AlumnoModel).where(AlumnoModel.id == id).first()
        alumnoActualizado = serializador.dump(resultado)
        
        return {
            'message': 'Alumno actualizado exitosamente',
            'content': alumnoActualizado

        }
    except ValidationError as error:
        return {
            'message': 'Error al actualizar el alumno',
            'content': error.args
        },400 # Mala solicitud | Bad Request
    
@app.route('/eliminar-alumno/<int:id>', methods = ['DELETE'])
def eliminarAlumno(id):
    alumnoEncontrado = conexion.session.query(AlumnoModel).with_entities(AlumnoModel.id).where(AlumnoModel.id == id).first()
    
    if not alumnoEncontrado:
        return {
            'message': 'El alumno no existe'
        }, 404
    
    conexion.session.query(AlumnoModel).where(AlumnoModel.id == id).delete()
    conexion.session.commit()

    return {
        'message': 'Alumno eliminado exitosamente'
    }

@app.route('/buscar-alumnos', methods = ['GET'])
def buscarAlumnos():
    # query params
    queryParams = request.args
    nombre = queryParams.get('nombre')
    correo = queryParams.get('correo')

    condiciones = []
    if nombre:
        # nombre = 'Mariana'
        # condiciones.append(AlumnoModel.nombre == nombre) # Busqueda exacta

        # nombre like '%Mar%'
        # condiciones.append(AlumnoModel.nombre.like(f"%{nombre}%")) # Busqueda por similitud

        # si queremos que la busqueda no respete mayusculas ni minusculas
        # i > insensitive
        condiciones.append(AlumnoModel.nombre.ilike(f"%{nombre}%"))

    if correo:
        # condiciones.append(AlumnoModel.correo == correo)
        condiciones.append(AlumnoModel.correo.ilike(f"%{correo}%"))

    # https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_
    resultado = conexion.session.query(AlumnoModel).where(and_(*condiciones)).all()

    # resultado = conexion.session.query(AlumnoModel).where(AlumnoModel.nombre == nombre, AlumnoModel.correo == correo).all()
    print(resultado)
    
    serializador = AlumnoSerializer()
    alumnos = serializador.dump(resultado,many=True)

    return {
        'content': alumnos
    }


# TODO EN ORM
# Crear una tabla llamada productos cuya clase sea ProductoModel
# id AI pk not null
# nombre texto not null
# precio float 
# disponible boolean
class ProductoModel(conexion.Model):
    id = Column(type_=types.Integer, autoincrement=True, primary_key=True, nullable=False)
    nombre = Column(type_=types.Text, nullable=False)
    precio = Column(type_=types.Float)
    disponible = Column(type_=types.Boolean)

    __tablename__='productos'


# flask --app 2-flask-con-orm:app db migrate -m "agregue tabla productos"
# flask --app 2-flask-con-orm:app db upgrade

# ingresar los siguientes valores

# INSERT INTO productos (nombre, precio, disponible) VALUES 
# ('Galleta de Ositos', 7.5, true), 
# ('Whiskas', 9.50, true), 
# ('Organizador', 25.30, true), 
# ('Ventilador de mano', 9.9, false), 
# ('Mouse inalambrico', 14.5, true);

class ProductoSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductoModel

# hacer una busqueda de los productos por su nombre (usando el ilike)
@app.route('/buscar-producto-por-nombre/<string:nombre>', methods=['GET'])
def buscarProductoPorNombre(nombre):
    productos = conexion.session.query(ProductoModel).where(ProductoModel.nombre.ilike(f"%{nombre}%"), ProductoModel.disponible == True).all()
    serializador = ProductoSerializer()
    
    resultado = serializador.dump(productos,many=True)
    
    return {
        'content': resultado
    }


# hacer otra busqueda de los productos en un rango de precio (precio minimo y precio maximo)
@app.route('/buscar-producto-por-precios/<int:minimo>/<int:maximo>', methods = ['GET'])
def buscarProductoPorPrecios(minimo, maximo):
    # Quiero los productos que cuesten entre 5 y 15 soles
    productos = conexion.session.query(ProductoModel).where(ProductoModel.precio >= minimo, ProductoModel.precio <= maximo , ProductoModel.disponible == True).all()
    serializador = ProductoSerializer()
    
    resultado = serializador.dump(productos,many=True)
    
    return {
        'content': resultado
    }

# en ambas busquedas solamente buscar los productos que esten disponibles

if __name__ == '__main__':
    app.run(debug=True)