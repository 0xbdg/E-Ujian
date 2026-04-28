from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field

GENDER = (("male", "Male"), ("female", "Female"))


class Account(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Student(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    photo = models.ImageField()
    grade = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=GENDER)


class Subject(models.Model):
    subject = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.subject


class Teacher(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    photo = models.ImageField()
    gender = models.CharField(max_length=50, choices=GENDER)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Exam(models.Model):
    course = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.course


class Question(models.Model):
    TYPE = (("multiple", "Multiple Choices"), ("essay", "Essay"))
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, choices=TYPE)


class Essay(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    question = CKEditor5Field("Text", config_name="extends")


class MultipleChoice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    question = CKEditor5Field("Text", config_name="extends")
    option1 = models.CharField(max_length=400)
    option2 = models.CharField(max_length=400)
    option3 = models.CharField(max_length=400)
    option4 = models.CharField(max_length=400)
    cat = (
        ("option1", "Option1"),
        ("option2", "Option2"),
        ("option3", "Option3"),
        ("option4", "Option4"),
    )
    answer = models.CharField(max_length=200, choices=cat)


class Result(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
