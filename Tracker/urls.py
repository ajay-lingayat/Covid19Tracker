from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('country', views.country, name="country"),
    path('country/<str:name>', views.country_name, name="country-name"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
]