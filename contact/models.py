from django.db import models
from django.core.validators import EmailValidator, RegexValidator

# Create your models here.


class ContactStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Contact(models.Model):
    # format: +48123456789, 123-456-789, etc.
    phone_regex = RegexValidator(
        regex=r'^\+?[\d\s().-]{5,25}$',
        message='Phone format: +99999999. Up to 15 digits.'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[phone_regex]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=[EmailValidator()]
    )
    city = models.CharField(max_length=60)
    status = models.ForeignKey(ContactStatus, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name
