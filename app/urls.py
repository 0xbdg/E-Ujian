from django.urls import path, include
from .views import *

urlpatterns = [
    path("accounts/login/", SigninView.as_view(), name="login"),
    path("soal-ujian/<int:pk>", StartExamView.as_view(), name="start-exam"),
    path("", HomeView.as_view(), name="home"),
]
