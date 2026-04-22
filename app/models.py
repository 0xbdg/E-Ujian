from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field


class Account(AbstractUser):
    ROLE = (("student", "Student"), ("teacher", "Teacher"), ("admin", "Admin"))
    role = models.CharField(max_length=50, choices=ROLE)


class Student(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    nis = models.BigIntegerField(null=False, blank=False)
    photo = models.ImageField()
    grade = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)


class Teacher(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    photo = models.ImageField()
    gender = models.CharField(max_length=50)


class Subject(models.Model):
    subject = models.CharField(max_length=500, null=False)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Exam(models.Model):
    course = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Question(models.Model):
    TYPE = (("multiple", "Multiple Choices"), ("essay", "Essay"))
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, choices=TYPE)
    question = CKEditor5Field("Text", config_name="extends")


class MultipleChoice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
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
    score = models.IntegerField(null=True, blank=True)
