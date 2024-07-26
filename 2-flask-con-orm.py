from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, types
# ORM una de las ventajas es que se usa para diferentes motores de base de datos por lo que si usamos uno en particular no podremos cambiar facilmente a otro motor de base de datos (postgre > mysql)
# from sqlalchemy.dialects.postgresql import 

app = Flask(__name__)
# se guardaran todas la configuraciones de nuestra aplicacion en Flask
# print(app.config)
# SQLALCHEMY cuando configuramos una base de datos que es postgres, utiliza el conector psycopg2 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@127.0.0.1:5432/colegio'
# busca la cadena de conexion a nuestra base de datos
conexion = SQLAlchemy(app) # configuracion hacia la base de datos

# asi se declara un modelo (tabla)
class AlumnoModel(conexion.Model):
    # type_ > tipo de dato de esa columna
    id = Column(type_=types.Integer, autoincrement=True, primary_key=True, nullable=False)
    nombre = Column(type_=types.Text, nullable=False)
    correo = Column(type_=types.Text, nullable=False, unique=True)
    fechaNacimiento = Column(name='fecha_nacimiento', type_=types.TIMESTAMP)

    # para indicar como se deberia llamar la tabla en la base de datos
    __tablename__ = 'alumnos'


@app.route('/')
def inicio():
    conexion.create_all() # crea todos los modelos que aun no existen en la base de datos, y si existen entonces los omite
    return {
        'message':'Bienvenido a mi API'
    }

@app.route('/crear-alumno', methods=['POST'])
def crearAlumno():
    data = request.get_json()
    # inicializo mi nuevo registro del alumno
    nuevoAlumno =  AlumnoModel(nombre = data['nombre'], correo = data['correo'], fechaNacimiento = data['fechaNacimiento'])
    
    print(nuevoAlumno.id)

    # agregarlo a la base de datos
    conexion.session.add(nuevoAlumno)

    # guardarlo de manera permanente
    conexion.session.commit()
    print(nuevoAlumno.id)

    return {
        'message': 'Alumno registrado exitosamente'
    }, 201 # Created (Creacion)

if __name__ == '__main__':
    app.run(debug=True)