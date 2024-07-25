from flask import Flask, request
# request > nos mostrara toda la info que nos envia el cliente

# __name__ > indicar si el archivo que estamos utilizando es el archivo principal del proyecto, esto se ve en la terminal ya que si al correr el proyecto llamamos a este archivo su valor sera __main__ caso contrario obtendra otro nombre
app = Flask(__name__)

@app.route('/')
def manejar_ruta_inicio():
    return 'Bienvenido a mi API de Flask!'

@app.route('/registrar-usuario',methods=['POST'])
def manejar_registro_usuario():
    print(request.get_json()) # convierte el json a un diccionario en python
    return {
        'message': 'Usuario Registrado exitosamente'
    }

if __name__ == '__main__':
    # estamos en el archivo principal

    # levanta mi servidor de flask
    # si configuramos el parametro debug en True cada vez que hagamos algun cambio y guardemos se reiniciara el servidor
    app.run(debug=True)