from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounts/login/', signin, name="login"),
    path('mulai-ujian/<int:pk>', mulai, name="start-exam"),
    path('', home, name='home')
]
