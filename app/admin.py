from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

from .models import *
from .forms import AuthenticationForm

class DashboardView(View):
    def get(self, request):
        return render(request, "admin/pages/dashboard.html")

class AdminLoginView(LoginView):
    template_name = "auth/admin_login.html"
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return redirect('')
