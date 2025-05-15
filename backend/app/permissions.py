from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Permiso personalizado que permite a los usuarios acceder a sus propios objetos.
    """

    def has_object_permission(self, request, view, obj):
        # Permitir acceso si el usuario es el propietario del objeto
        return obj.cliente_id == request.user.id

class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado que permite a los administradores acceder a todos los objetos.
    """

    def has_permission(self, request, view):
        # Permitir acceso si el usuario es un administrador
        return request.user.is_admin
