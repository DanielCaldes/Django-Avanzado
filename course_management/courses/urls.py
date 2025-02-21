from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UsersCreateGetView, UsersGetDeleteView, CategoryListView, CategoryRetrieveView, CourseUpdateView, ResetPasswordView

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'materials', views.MaterialCourseViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'grades', views.GradeViewSet)
router.register(r'forums', views.ForumViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'feedback', views.CourseFeedbackViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/users/', UsersCreateGetView.as_view(), name='user_detail'),
    path('api/users/<int:user_id>/', UsersGetDeleteView.as_view(), name='user_detail'),
    path('api/users/<int:user_id>/password/', ResetPasswordView.as_view(), name='reset-password'),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryRetrieveView.as_view(), name='category-detail'),
    path('api/courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
]