from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.profile_picture = request.FILES.get('profile_picture')
        user.save()
        return redirect('profile')