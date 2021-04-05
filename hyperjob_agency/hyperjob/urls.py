from django.urls import path
from resume.views import MainView, ResumesView, AuthView, SignUpView, HomeView, NewResumeView
from vacancy.views import VacanciesView, NewVacancyView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', MainView.as_view()),
    path('home', HomeView.as_view()),
    path('resumes/', ResumesView.as_view()),
    path('vacancies/', VacanciesView.as_view()),
    path('resume/new', NewResumeView.as_view()),
    path('vacancy/new', NewVacancyView.as_view()),
    path('login', AuthView.as_view()),
    path('signup', SignUpView.as_view()),
    path('logout', LogoutView.as_view()),
]

urlpatterns += static(settings.STATIC_URL)