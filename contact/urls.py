from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('contact/<str:pk>/', views.contact, name='contact'),
    path('create-contact/', views.createContact, name='create-contact'),
    path('edit-contact/<str:pk>/', views.updateContact, name='update-contact'),
    path('delete-contact/<str:pk>/', views.deleteContact, name='delete-contact'),
    path('import-contacts/', views.importContacts, name='import-contacts'),
]
