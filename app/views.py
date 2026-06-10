from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from datetime import datetime
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

        context["exam_count"] = Exam.objects.count(),
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
        efinish = ExamFinish.objects.get(student=request.user, exam=pk)
        types = None
        c = None
        time_e = Exam.objects.get(id=pk).end_time
        time_s = datetime.now()


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
                "time_start": ((time_s.hour * 3600) + (time_s.minute * 60) + time_s.second),
                "time_end":((time_e.hour * 3600) + (time_e.minute * 60) +time_e.second),
                "is_ended": efinish.finished
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

        ExamFinish(student=request.user, exam=get_object_or_404(Exam, id=pk), finished=True).save()

        #return HttpResponse(test)
        return redirect("home")


class DashboardView(View):
    def get(self, request):
        return render(request, "superuser/pages/dashboard.html")
