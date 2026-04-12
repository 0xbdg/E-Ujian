from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.views import View
from django.views.generic import FormView, ListView, DetailView
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


class HomeView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = "client/pages/home.html"
    paginate_by = 5
    context_object_name = "exams"


class ConfirmationView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "client/pages/confirm_exam.html"
    context_object_name = "exam"


def mulai_ujian(request, pk):
    matapelajaran = Exam.objects.get(id=pk)
    question = matapelajaran.objects.all()

    paginator = Paginator(question, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        if "submit" in request.POST:
            responses = {}
            for question in page_obj:
                question_id = question.id
                answer = request.POST.get(f"question_{question_id}")
                if answer:
                    responses[question_id] = answer

        else:
            for question in page_obj:
                question_id = question.id
                answer = request.POST.get(f"question_{question_id}")
                if answer:
                    response = HttpResponse("Your answers are saved.")
                    response.set_cookie(
                        f"question_{question_id}", answer, max_age=3600
                    )                      return response

    return render(
        request,
        "pages/start_exam.html",
        context={"matapelajaran": matapelajaran, "page_obj": page_obj},
    )
