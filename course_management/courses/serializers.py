from rest_framework import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_professor = serializers.BooleanField(write_only=True, required=False, default=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_professor']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseUpdateView(generics.UpdateAPIView):  # Permite modificar un curso
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Student
        fields = ['user', 'course']

class MaterialCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = MaterialCourse
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    materials = MaterialCourseSerializer(many=True, required=False)

    class Meta:
        model = Activity
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    activity = ActivitySerializer()

    class Meta:
        model = Grade
        fields = '__all__'

class ForumSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Forum
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    forum = ForumSerializer()

    class Meta:
        model = Post
        fields = '__all__'

class CourseFeedbackSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    student = StudentSerializer() 

    class Meta:
        model = CourseFeedback
        fields = '__all__'