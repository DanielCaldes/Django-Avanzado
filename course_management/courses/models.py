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


class MaterialCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=200)
    file_path = models.CharField(max_length=500, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.name}"

class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="activities")
    title = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    due_date = models.DateTimeField()
    max_grade = models.DecimalField(max_digits=5, decimal_places=2)
    materials = models.ManyToManyField(MaterialCourse, related_name="activities", blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_activity_type_display()})"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="grades")
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.activity.title}: {self.grade}"

class Forum(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forum: {self.title} - {self.course.name}"

class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} in {self.forum.title}"

class CourseFeedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} Rating: {self.rating}"
