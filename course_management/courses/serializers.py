from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    is_professor = serializers.BooleanField(write_only=True, required=True) #auxiliar para indicar el grupo al que pertenece

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_professor']

    def create(self, validated_data):
        # Eliminar los datos auxiliares
        is_professor = validated_data.pop('is_professor')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password) # Para pasarla de forma segura
        user.save()

        # Asignar el grupo
        group_name = "Professors" if is_professor else "Students"
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        return user

class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6, required=True)

class CourseSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, write_only=True)
    categories_details = CategorySerializer(source='categories', read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'user_username', 'created_at']

