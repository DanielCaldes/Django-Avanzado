from django.shortcuts import render

from rest_framework import viewsets
from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsProfessor, IsProfessorOrReadOnly, ReadOnlyForStudents, IsAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group

# Category 
# Ver todas las categorias
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
# Consultar una categoria por id
class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UsersCreateGetView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            data=[]
            for user in users:
                data.append(
                    {
                        "id":user.id,
                        "username" : user.username,
                        "email" : user.email,
                        "professor" : user.groups.filter(name="Students").exists()
                    }
                )
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        is_professor = request.data.get("is_professor")

        required_fields = ["username", "email", "password"]
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        if missing_fields:
            return Response(
                {"message": "All fields are required", "missing_fields": missing_fields}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        print("He creado un alumno")
        user = User.objects.create_user(username=username, email=email, password=password)

        group_name = "Professors" if is_professor == True else "Students"
        print(group_name)
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return Response({"message": "User created successfully", "id": user.id}, status=status.HTTP_201_CREATED)
    
class UsersGetDeleteView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id = user_id)
            data = {
                "id":user.id,
                "username" : user.username,
                "email" : user.email
            }
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, user_id):
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"message": "Missing 'new_password' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)

            user.set_password(new_password)

            user.save()

            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class MaterialCourseViewSet(viewsets.ModelViewSet):
    queryset = MaterialCourse.objects.all()
    serializer_class = MaterialCourseSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CourseFeedbackViewSet(viewsets.ModelViewSet):
    queryset = CourseFeedback.objects.all()
    serializer_class = CourseFeedbackSerializer

class SuggestionsGetView(APIView):
    def get(self, request):
        if 'student_id' not in request.query_params:
            return Response({"detail": "Missing student_id parameter."}, status=status.HTTP_400_BAD_REQUEST)

        student_id = request.query_params['student_id']
        
        try:
            student = Student.objects.get(id=student_id)

            # Obtener las categorías de los cursos en los que el estudiante está inscrito
            student_courses = student.courses.all()
            categories = set()
            for course in student_courses:
                categories.update(course.categories.all())  # Usamos ManyToMany para obtener las categorías

            # Buscar otros cursos que pertenezcan a las mismas categorías
            suggested_courses = Course.objects.filter(categories_in=categories).exclude(id_in=student_courses.values_list('id', flat=True))

            if not suggested_courses.exists():
                return Response({"detail": "No course suggestions found."}, status=status.HTTP_404_NOT_FOUND)

            suggested_courses_list = [{"name": course.name, "description": course.description} for course in suggested_courses]

            return Response({
                "suggested_courses": suggested_courses_list
            }, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)