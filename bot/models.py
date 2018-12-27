import datetime
from django.db import models


class Question(models.Model):
    text = models.CharField(blank=True, unique=True, default='', max_length=250)
    have_choices = models.BooleanField(default=False, blank=True)
    next = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True)
    is_start_question = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


# Create your models here.
class User(models.Model):
    # user_id = models.AutoField(unique=True, primary_key=True)
    chat_id = models.IntegerField(unique=True, default='0')
    chat = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    # specialty = models.CharField(max_length=250, blank=True)
    # programm_language = models.CharField(max_length=250, blank=True)
    # fio = models.CharField(max_length=250, blank=True)
    # phone = models.CharField(max_length=250, blank=True)
    # email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
    # study = models.CharField(max_length=250, blank=True)
    # skills = models.TextField(max_length=4096, blank=True)
    # time_work = models.TextField(max_length=4096, blank=True)
    # schedule = models.TextField(max_length=4096, blank=True)
    # question = models.CharField(blank=True, default='0', max_length=250)
    current_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Choices(models.Model):
    text = models.CharField(blank=True, default='', max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_choice')
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_before_choice')

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):
    text = models.CharField(blank=True, default='', max_length=4096)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'
