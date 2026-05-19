from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
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
        context["exam_active"] = Exam.objects.filter(
            start_date__lte=datetime.datetime.now()
        )
        context["exam_ended"] = Exam.objects.filter(
            end_date__gte=datetime.datetime.now()
        )
        context["exam_inactive"] = Exam.objects.filter(
            start_date__gte=datetime.datetime.now()
        )
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

        data = request.POST.items()
        test = []

        for var, val in data:
            if var.startswith("jawaban_"):

                test.append(val)

                Result(
                    student_id=request.user,
                    question_id=Question.objects.get(id=pk),
                    answer=val,
                ).save()

        return HttpResponse(test)


class DashboardView(View):
    def get(self, request):
        return render(request, "superuser/pages/dashboard.html")
