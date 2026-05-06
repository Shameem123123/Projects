from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text')
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)