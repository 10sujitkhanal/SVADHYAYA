from django.views.generic import TemplateView, DetailView, View
from django.shortcuts import render

class SolverView(View):
    def get(self, request):
        return render(request, 'solver/home.html')
        