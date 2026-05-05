from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import FormView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import *
from .models import *
from .mixin import *

import datetime

# Create your views here.


class SigninView(LoginView):
    template_name = "auth/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse_lazy("home")
        if user.is_teacher and user.is_staff:
            return reverse_lazy("home")
        if user.is_student:
            return reverse_lazy("home")


class HomeView(ListView):
    model = Exam
    template_name = "client/pages/home.html"
    paginate_by = 9
    queryset = Exam.objects.order_by("-id")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context["exam_count"] = Exam.objects.count()
        context["exams"] = Exam.objects.all()
        context["date"] = datetime.datetime.now()
        return context


class StartExamView(View):
    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        mc = None
        c = None

        if question.question_type == "multiple":
            mc = MultipleChoice.objects.filter(question_id=question.id)
            c = MultipleChoice.objects.count()
        elif question.question_type == "essay":
            mc = Essay.objects.filter(question_id=question.id)
            c = Essay.objects.count()

        return render(
            request,
            "client/pages/start_exam.html",
            {
                "question": question,
                "choices": mc,
                "count": c,
            },
        )

    def post(self, request, pk):
        data = request.POST

        Result().save()


class DashboardView(View):
    def get(self, request):
        return render(request, "superuser/pages/dashboard.html")


"""
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
    )"""
