from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required
def home(request):
    exam = Exam.objects.all()
    paginator = Paginator(exam, 5)
    page_num = request.GET.get('page')
    page_object = paginator.get_page(page_num)
    return render(request, 'pages/home.html', context={'exams':page_object})