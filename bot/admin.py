from django.contrib import admin

# Register your models here.
from bot.models import User, Question, Choices, Answer

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Choices)
admin.site.register(Answer)