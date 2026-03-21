from django.views import View
from django.shortcuts import render, redirect

from .models import *

class DashboardView(View):
    def get(self, request):
        return render(request, "admin/pages/dashboard.html")

