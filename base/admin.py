from django.contrib import admin
from .models import Profile, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Profile)
admin.site.register(Question, QuestionAdmin)
