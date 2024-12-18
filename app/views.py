from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.http import HttpResponse

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

@login_required
def konfirmasi(request, pk):
    exam = Exam.objects.get(id=pk)

    return render(request, "pages/confirm_exam.html", context={'exam':exam})

@login_required
def mulai_ujian(request, pk):
    matapelajaran = Exam.objects.get(id=pk)
    question = matapelajaran.objects.all()

    paginator = Paginator(question, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        if 'submit' in request.POST:
            responses = {}
            for question in page_obj:
                question_id = question.id
                answer = request.POST.get(f'question_{question_id}')
                if answer:
                    responses[question_id] = answer
            
        else:
            for question in page_obj:
                question_id = question.id
                answer = request.POST.get(f'question_{question_id}')
                if answer:
                    # Save the answer in a cookie with the question id as key
                    response = HttpResponse("Your answers are saved.")
                    response.set_cookie(f'question_{question_id}', answer, max_age=3600)  # Cookie valid for 1 hour
                    return response



    return render(request, 'pages/start_exam.html', context={"matapelajaran":matapelajaran, "page_obj":page_obj})