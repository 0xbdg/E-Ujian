from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounts/login/', SigninView.as_view(), name="login"),
    path('konfirmasi-ujian/<int:pk>', konfirmasi, name="confirm-exam"),
    path('soal-ujian/<int:pk>', mulai_ujian, name="start-exam"),
    path('', HomeView.as_view(), name='home')
]
