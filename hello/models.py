from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
	
class Tempmedia(models.Model):
    file_name = models.CharField(max_length=50)
    working = models.BooleanField(default=False)
    status = models.PositiveIntegerField(default=0)
    url = models.CharField(max_length=150)
    when = models.DateTimeField(auto_now=True)
