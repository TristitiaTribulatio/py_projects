from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index),
    path("news/", views.main),
    path("news/create/", views.create),
    path("news/<int:num>/", views.news),
]

urlpatterns += static(settings.STATIC_URL)