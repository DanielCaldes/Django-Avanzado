from django.shortcuts import render

from rest_framework import viewsets
from .models import *
from .serializers import *

from rest_framework import generics

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsAdminUserOrProfessorOrReadOnly,IsProfessor, IsProfessorOrReadOnly, ReadOnlyForStudents, IsStudent

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from django.contrib.auth.models import User

###############
#   CATEGORY  #
###############

# View all categories
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Query a category by ID
class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


###############
#    USERS    #
###############

# Prevent code duplication when formatting the user data output for JSON
def format_user_data(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "professor": user.groups.filter(name="Professors").exists(),
    }

# Create and retrieve the user list.
class UsersListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by teachers if '/?is_teacher=true' or students '/?is_teacher=false' is provided.
        is_professor = self.request.query_params.get("is_professor")
        if is_professor is not None:
            group_name = "Professors" if is_professor.lower() == "true" else "Students"
            queryset = queryset.filter(groups__name=group_name)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [
            format_user_data(user) for user in queryset
        ]
        return Response(data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {"message": "User created successfully", "id": user.id},
            status=status.HTTP_201_CREATED,
        )
    
# Get and delete a user by ID    
class UsersRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = format_user_data(instance)
        return Response(data, status=status.HTTP_200_OK)

# Reset a password
class PasswordUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PasswordUpdateSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            return Response({"message": "The password has been successfully updated."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###############
#   COURSES   #
###############

# Allows performing all basic operations on the course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUserOrProfessorOrReadOnly]

# Allows adding users to the course and viewing the course user list
class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Student.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(course=course)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        student_id = response.data.get('id')
        return Response(
            {"detail": f"Successfully created. Student ID: {student_id}"},
            status=status.HTTP_201_CREATED
        )

# Allows deleting users
class StudentDestroyView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        student_id = self.kwargs['pk'] 
        student = Student.objects.filter(id=student_id).first()

        if not student:
            raise NotFound(detail="No student with that id.")
        
        return student

# Suggest courses to users with sames categories to the ones they are enrolled in
class SuggestionsGetView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({"detail":"User not found."}, status=status.HTTP_404_NOT_FOUND)

            students = Student.objects.filter(user=user)

            if not students.exists():
                return Response({"detail":"User is not enrolled in any of the courses."}, status=status.HTTP_404_NOT_FOUND)
           
            # Get the IDs of the courses the user is enrolled in
            student_courses_ids = students.values_list('course', flat=True)
            
            # Get the categories of those courses, using distinct to ensure there are no duplicates
            categories = Course.objects.filter(id__in=student_courses_ids).values_list('categories', flat=True).distinct()

            # Search for other courses that belong to the same categories, and exclude the ones the student is already enrolled in
            suggested_courses = Course.objects.filter(categories__in=categories).exclude(id__in=student_courses_ids).distinct()

            if not suggested_courses.exists():
                return Response({"detail": "No course suggestions found."}, status=status.HTTP_404_NOT_FOUND)

            suggested_courses_list = [{
                "name": course.name, 
                "description": course.description, 
                "categories": [category.name for category in course.categories.all()]}
                  for course in suggested_courses]

            return Response({
                "suggested_courses": suggested_courses_list
            }, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
