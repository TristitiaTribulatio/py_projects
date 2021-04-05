from django.shortcuts import render, redirect
from django.views import View
from .models import Resume
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.http import HttpResponseForbidden
from django import forms


class MainView(View):
    @staticmethod
    def get(request):
        return render(request, "main.html", {})


class ResumesView(View):
    @staticmethod
    def get(request):
        return render(request, "resumes.html", context={"resumes": Resume.objects.all()})


class AuthView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class HomeView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return render(request, 'home.html', {})
        else:
            return redirect('/login')


class NewResumeView(View):
    @staticmethod
    def post(request):
        form = AddForm(request.POST)
        if form.is_valid():
            clean_form = dict(form.cleaned_data)
            description = clean_form['description']
            if request.user.is_authenticated and not request.user.is_staff:
                Resume(description=description, author=request.user).save()
                return redirect('/home')
            else:
                return HttpResponseForbidden()
        return HttpResponseForbidden()


class AddForm(forms.Form):
    description = forms.CharField(max_length=1024)
