from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    professor_id = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Professors'})
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(Category, related_name='courses', blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        user_str = self.user.username if self.user else "No User"
        course_str = self.course.name if self.course else "No Course"
        return f"{user_str} - {course_str}"

