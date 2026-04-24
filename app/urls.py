from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("accounts/login/", SigninView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("soal-ujian/<int:pk>/", StartExamView.as_view(), name="start-exam"),
    path("admin/dashboard/", DashboardView.as_view(), name="admin-dashboard"),
    path("", HomeView.as_view(), name="home"),
]
