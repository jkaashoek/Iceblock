from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Course(models.Model):
    description = models.CharField(max_length=900)
    name = models.CharField(max_length=900)
    teacher = models.CharField(max_length=900)
    max_cap = models.IntegerField(max_length=900)
    available = models.CharField(max_length=900)
    preferences = []
    def __unicode__(self):
        return self.name
    
class UserProfile(models.Model):
    #required by the auth model
    user = models.ForeignKey(User, unique=True)
    school = models.CharField(max_length=30)
    grade = models.IntegerField(max_length=2, null=True, blank=True)
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    option5 = models.CharField(max_length=50)

class Assignment(models.Model):
    user = models.ForeignKey(User, unique=False)
    class_name = models.CharField(max_length=900)
    

