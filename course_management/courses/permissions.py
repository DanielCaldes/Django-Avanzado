from rest_framework import permissions

class IsAdminUserOrProfessorOrReadOnly(permissions.BasePermission):
    """
    Permite si el usuario es un administrador o un profesor
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:  
            return True
        
        return request.user.is_staff or request.user.groups.filter(name="Professors").exists()

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

class IsStudent(permissions.BasePermission):
    """
    Permiso para estudiantes
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Students').exists()

class ReadOnlyForStudents(permissions.BasePermission):
    """
    Permiso para permitir solo lectura a los estudiantes.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Permite lectura a todos
        return request.user and not request.user.groups.filter(name='Students').exists()