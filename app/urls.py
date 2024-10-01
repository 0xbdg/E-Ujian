from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounts/login/', signin, name="login"),
    path('konfirmasi-ujian/<int:pk>', konfirmasi, name="confirm-exam"),
    path('soal-ujian/<int:pk>', mulai_ujian, name="start-exam"),
    path('', home, name='home')
]
