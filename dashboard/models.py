from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def str(self):
        return str(self.id)

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due = models.DateTimeField()
    is_finish = models.BooleanField(default=False)

    def str(self):
        return str(self.id)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_finish = models.BooleanField(default=False)

    def str(self):
        return str(self.id)

class Contact(models.Model):
    
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    contact = models.PositiveIntegerField()
    feedback = models.TextField()

    def str(self):
        return str(self.id)
