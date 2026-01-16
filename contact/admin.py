from django.contrib import admin
from .models import Contact, ContactStatus

# Register your models here.
admin.site.register(Contact)
admin.site.register(ContactStatus)
