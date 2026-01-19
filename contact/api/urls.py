from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('contacts/', views.getContacts),
]
