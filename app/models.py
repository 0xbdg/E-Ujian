from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Exam(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = CKEditor5Field("Question")
    option1 = models.CharField(max_length=400)
    option2 = models.CharField(max_length=400)
    option3 = models.CharField(max_length=400)
    option4 = models.CharField(max_length=400)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer = models.CharField(max_length=200, choices=cat)

    def __str__(self):
        return self.question
