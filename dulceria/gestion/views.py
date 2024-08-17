from django.shortcuts import render


def paginaPrueba(request):
    print(request)
    data = [{
        "id": 1,
        "nombre": "Importados",
        "habilitado": True
    }, {
        "id": 2,
        "nombre": "Nacionales",
        "habilitado": False
    }]

    usuario = 'Eduardo'

    return render(request, 'prueba.html', {"data": data, "usuario": usuario})
