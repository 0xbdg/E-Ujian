from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate,login
from django.views import View 
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *

# Create your views here.

class SigninView(LoginView):
    template_name = "auth/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user

        return reverse_lazy("home")

class HomeView(LoginRequiredMixin,ListView):
    model = Exam
    template_name = "client/pages/home.html"
    paginate_by = 5 
    context_object_name = "exams"

def home(request):
    exam = Exam.objects.all()
    paginator = Paginator(exam, 5)
    page_num = request.GET.get('page')
    page_object = paginator.get_page(page_num)
    return render(request, 'client/pages/home.html', context={'exams':page_object})


def konfirmasi(request, pk):
    exam = Exam.objects.get(id=pk)

    return render(request, "client/pages/confirm_exam.html", context={'exam':exam})

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
