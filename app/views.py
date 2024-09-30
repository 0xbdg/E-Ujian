from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout

from .forms import *
from .models import *

# Create your views here.

@login_required
def home(request):
    exam = Exam.objects.all()
    paginator = Paginator(exam, 5)
    page_num = request.GET.get('page')
    page_object = paginator.get_page(page_num)
    return render(request, 'pages/home.html', context={'exams':page_object})

def signin(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', context={'form':form})