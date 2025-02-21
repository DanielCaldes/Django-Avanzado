from rest_framework import permissions

class IsProfessor(permissions.BasePermission):
    """
    Permission for users in group 'Professor'.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Professor').exists()
    
class IsProfessorOrReadOnly(permissions.BasePermission):
    """
    Allows read access to all authenticated users, but only users in the 'Professor' group can modify.
    """

    def has_permission(self, request, view):
        # Permitir GET, HEAD, OPTIONS a cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Para otros métodos (POST, PUT, DELETE), verificar si es profesor
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Professor').exists()    
    
class ReadOnlyForStudents(permissions.BasePermission):
    """
    Permiso para permitir solo lectura a los estudiantes.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Permite lectura a todos
        return request.user and not request.user.groups.filter(name='Students').exists()
    
class IsAdmin(permissions.BasePermission):
    """
    Permission for admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff