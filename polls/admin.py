from django.contrib import admin

from .models import Choice, Question, SuggestedChoice, Comment

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(SuggestedChoice)
admin.site.register(Comment)
