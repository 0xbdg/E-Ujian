from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounts/login/', signin, name="login"),
    path('', home, name='home')
]
