
from django.contrib.auth.models import Permission, User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=250)
    college = models.CharField(max_length=500)
    course = models.CharField(max_length=100)
    photo = models.FileField()
    answer=models.BooleanField(default=False)
    def __str__(self):
        return self.name + ' - ' + self.college


class Marks_card(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    semester = models.CharField(max_length=250)
    marks_card = models.FileField(default='')
    
    def __str__(self):
        return self.semester


class Vote(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    answer=models.BooleanField(default=False)
    
    