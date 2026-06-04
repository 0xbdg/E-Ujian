from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from .forms import *
from .models import *
from .mixin import *


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context["exam_count"] = Exam.objects.count()
        context["exam_active"] = Exam.objects.filter(
            start_time__lte=timezone.localtime().time(),
            end_time__gte=timezone.localtime().time()
        )
        context["exam_ended"] = Exam.objects.filter(
            end_time__lte=timezone.localtime().time()
        )
        context["exam_inactive"] = Exam.objects.filter(
            start_time__gte=timezone.localtime().time()
        )
        return context


class StartExamView(View):
    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        types = None
        c = None

        if question.question_type == "multiple":
            types = MultipleChoice.objects.filter(question_id=question.id)
            c = MultipleChoice.objects.count()
        elif question.question_type == "essay":
            types = Essay.objects.filter(question_id=question.id)
            c = Essay.objects.count()

        return render(
            request,
            "client/pages/start_exam.html",
            {
                "question": question,
                "choices": types,
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

        ExamFinish(student_id=request.user.username, exam_id=Exam.objects.get(id=pk).course, finished=True).save()


        return HttpResponse(test)


class DashboardView(View):
    def get(self, request):
        return render(request, "superuser/pages/dashboard.html")
