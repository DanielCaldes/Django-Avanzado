from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UsersListCreateView, UsersRetrieveDeleteView, PasswordUpdateView
from .views import CategoryListView, CategoryRetrieveView
from .views import StudentListCreateView, StudentDestroyView
from .views import SuggestionsGetView

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path('api/users/', UsersListCreateView.as_view(), name='user_detail'),
    path('api/users/<int:pk>/', UsersRetrieveDeleteView.as_view(), name='user_detail'),
    path('api/users/<int:pk>/password/', PasswordUpdateView.as_view(), name='reset-password'),
    path('api/users/<int:user_id>/suggestions/',SuggestionsGetView.as_view(), name='suggestions'),

    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryRetrieveView.as_view(), name='category-detail'),

    path('api/courses/<int:course_id>/students/', StudentListCreateView.as_view(), name='course-students'),
    path('api/courses/<int:course_id>/students/<int:pk>/', StudentDestroyView.as_view(), name='delete-student'),
]