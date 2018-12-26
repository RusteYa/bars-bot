import datetime
from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(unique=True, primary_key=True)
    chat_id = models.IntegerField(unique=True, default='0')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    update_id = models.IntegerField(unique=True)
    specialty = models.CharField(max_length=250)
    programm_language = models.CharField(max_length=250)
    fio = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    study = models.CharField(max_length=250)
    skills = models.TextField(max_length=4096)
    time_work = models.TextField(max_length=4096)
    schedule = models.TextField(max_length=4096)
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f'{self.sender}'
