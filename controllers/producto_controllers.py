from instancias import conexion
from models import ProductoModel
from flask_restful import Resource, request
from serializers import ProductoSerializer
from marshmallow.exceptions import ValidationError
from utilitarios import serializadorPaginacion

class ProductosController(Resource):
    def post(self):
        data = request.get_json()
        serializador = ProductoSerializer()
        try:
            dataSerializada = serializador.load(data)
            nuevoProducto = ProductoModel(**dataSerializada)
            conexion.session.add(nuevoProducto)
            conexion.session.commit()

            resultado = serializador.dump(nuevoProducto)
            return {
                'message': 'Producto creado exitosamente',
                'content': resultado
            }
        except ValidationError as error:
            return {
                'message': 'Error al crear el producto',
                'content': error.args
            }
        
    def get(self):
        queryParams = request.args
        # Para la paginacion es necesario saber pagina que vamos a ubicarnos y cuantos elementos por pagina quiere el frontend
        page = int(queryParams.get('page', 1))
        perPage = int(queryParams.get('perPage', 5))

        # cantidad de elementos que debo de saltar 
        offset = (page - 1 ) * perPage
        limit = perPage
        
        totalProductos = conexion.session.query(ProductoModel).count()
        productos = conexion.session.query(ProductoModel).offset(offset).limit(limit).all()

        informacionPaginacion = serializadorPaginacion(total= totalProductos,pagina= page, porPagina= perPage)

        serializador = ProductoSerializer()
        resultado = serializador.dump(productos, many=True)

        return {
            'content': resultado,
            'pagination': informacionPaginacion
        }