from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('contact/<str:pk>/', views.contact, name='contact'),
    path('create-contact/', views.createContact, name='create-contact')
]
