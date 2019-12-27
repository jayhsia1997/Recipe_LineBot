from django.urls import path, include
from django.conf.urls import url

from Fit_Foodie import views

urlpatterns = [
    url(r'^callback', views.callback),
]