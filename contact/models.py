from django.db import models

# Create your models here.


class ContactStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    city = models.CharField(max_length=60)
    status = models.ForeignKey(ContactStatus, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', '-created']

    def __str__(self):
        return self.first_name
