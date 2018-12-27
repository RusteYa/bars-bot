import datetime
from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(unique=True, primary_key=True)
    chat_id = models.IntegerField(unique=True, default='0')
    chat = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    specialty = models.CharField(max_length=250, blank=True)
    programm_language = models.CharField(max_length=250, blank=True)
    fio = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
    study = models.CharField(max_length=250, blank=True)
    skills = models.TextField(max_length=4096, blank=True)
    time_work = models.TextField(max_length=4096, blank=True)
    schedule = models.TextField(max_length=4096, blank=True)
    question = models.CharField(blank=True, default='0', max_length=250)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

