from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category
from django.contrib.auth.models import Group

@receiver(post_migrate)
def crear_grupos_por_defecto(sender, **kwargs):
    Group.objects.get_or_create(name="Professors")
    Group.objects.get_or_create(name="Students")

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    categories = [
    ('programming', 'Programming'),
    ('data_science', 'Data Science'),
    ('design', 'Design'),
    ('marketing', 'Marketing'),
    ('business', 'Business'),
    ('cybersecurity', 'Cybersecurity'),
    ('cloud_computing', 'Cloud Computing'),
    ('artificial_intelligence', 'Artificial Intelligence'),
    ('machine_learning', 'Machine Learning'),
    ('web_development', 'Web Development'),
    ('mobile_app_development', 'Mobile App Development'),
    ('game_development', 'Game Development'),
    ('devops', 'DevOps'),
    ('big_data', 'Big Data'),
    ('iot', 'Internet of Things'),
    ]
    for category in categories:
        Category.objects.get_or_create(name=category[0])
