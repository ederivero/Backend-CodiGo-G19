from flask import Flask, request
# request > nos mostrara toda la info que nos envia el cliente
from psycopg import connect

# connect > nos permite conectarnos a la base de datos
# connection string: dialecto://user:password@host:port/db_name
# conexion = connect(conninfo='postgresql://postgres:@localhost:5432/bd_flask')
conexion = connect(conninfo='postgresql://admin:root@localhost:5432/bd_flask')

# __name__ > indicar si el archivo que estamos utilizando es el archivo principal del proyecto, esto se ve en la terminal ya que si al correr el proyecto llamamos a este archivo su valor sera __main__ caso contrario obtendra otro nombre
app = Flask(__name__)

@app.route('/')
def manejar_ruta_inicio():
    return 'Bienvenido a mi API de Flask!'

@app.route('/registrar-usuario',methods=['POST'])
def manejar_registro_usuario():
    print(request.get_json()) # convierte el json a un diccionario en python
    data = request.get_json() # {"nombre": "ajaja", "apellido": "jejeje", correo: "jijijij" }
    cursor = conexion.cursor() # podemos interactuar con la base de datos (escribir y leer la informacion de la bd)
    # %s > convierte el texto a string 
    cursor.execute("INSERT INTO usuarios (nombre, apellido, correo) VALUES (%s, %s, %s)", (data['nombre'], data['apellido'], data['correo']))

    # para que los cambios se guarden de manera permanente se tiene que realizar un commit a la base de datos (como las transacciones)
    # si queremos que esto sea de manera automatica podemos indicar en el connect el parametro autocommit=True
    conexion.commit()
    cursor.close() # cerramos la interaccion con la tabla para evitar bloqueos innecesarios

    return {
        'message': 'Usuario Registrado exitosamente'
    }

@app.route('/listar-usuarios', methods = ['GET'])
def devolver_usuarios():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    # fetchall() > retorna todos los registros leidos
    # fetchone() > me retorna el primer registro
    # fetchmany(NUM_REGSTROS) > cuantos registros quiero leer
    usuarios = cursor.fetchall()
    print(usuarios)

    resultado = []

    for usuario in usuarios:
        usuario_dic = {
            'id': usuario[0],
            'nombre': usuario[1],
            'apellido': usuario[2],
            'correo': usuario[3]
        }

        resultado.append(usuario_dic)
    return {
        'content': resultado
    }

if __name__ == '__main__':
    # estamos en el archivo principal

    # levanta mi servidor de flask
    # si configuramos el parametro debug en True cada vez que hagamos algun cambio y guardemos se reiniciara el servidor
    app.run(debug=True)