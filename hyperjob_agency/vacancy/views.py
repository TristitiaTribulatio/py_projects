from django.shortcuts import render, redirect
from django.views import View
from .models import Vacancy
from django.http import HttpResponseForbidden
from django import forms


class VacanciesView(View):
    @staticmethod
    def get(request):
        return render(request, "vacancies.html", context={"vacancies": Vacancy.objects.all()})


class NewVacancyView(View):
    @staticmethod
    def post(request):
        form = AddForm(request.POST)
        if form.is_valid():
            clean_form = dict(form.cleaned_data)
            description = clean_form['description']
            if request.user.is_authenticated and request.user.is_staff:
                Vacancy(description=description, author=request.user).save()
                return redirect('/home')
            else:
                return HttpResponseForbidden()
        return HttpResponseForbidden()


class AddForm(forms.Form):
    description = forms.CharField(max_length=1024)
