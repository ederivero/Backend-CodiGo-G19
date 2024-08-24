from rest_framework import permissions


class EsAdministrador(permissions.BasePermission):
    # Si queremos cambiar el mensaje en el caso no tenga los permisos necesarios
    message = 'Lo sentimos pero aca solo pueden ingresar administradores'

    def has_permission(self, request, view):
        print(view)
        tipo_usuario = request.user.tipoUsuario
        print(tipo_usuario)

        if tipo_usuario == 'ADMIN':
            return True
        # si retornamos True entonces significara que cumple con los permisos validos
        # si retornamos False no tiene los permisos suficientes
        else:
            return False
