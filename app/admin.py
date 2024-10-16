from django.contrib import admin
from .models import *

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class ExamAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'end_date']
    inlines = [QuestionInline]

# Register your models here.
admin.site.register(Exam, ExamAdmin)