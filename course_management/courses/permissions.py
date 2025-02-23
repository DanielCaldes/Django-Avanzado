from rest_framework import permissions

class IsAdminUserOrProfessorOrReadOnly(permissions.BasePermission):
    """
    Allow if the user is an administrator or a teacher.
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
        # GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # POST, PUT, DELETE
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Professor').exists()    

class IsStudent(permissions.BasePermission):
    """
    Permission for users in group 'Students'
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Students').exists()

class ReadOnlyForStudents(permissions.BasePermission):
    """
    Permission to allow read-only access for students.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and not request.user.groups.filter(name='Students').exists()