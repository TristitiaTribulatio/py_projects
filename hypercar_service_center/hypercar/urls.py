from django.urls import path
from tickets.views import MenuView, TicketView, OperatorView, NextView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('menu/', MenuView.as_view()),
    path('get_ticket/<str:service>', TicketView.as_view()),
    path('processing', OperatorView.as_view()),
    path('next', NextView.as_view()),
]

urlpatterns += static(settings.STATIC_URL)