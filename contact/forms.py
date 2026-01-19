from django.forms import ModelForm
from django import forms
from django.core.validators import FileExtensionValidator
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class ImportContactsForm(forms.Form):
    file = forms.FileField(
        help_text="Format: Only CSV files",
        widget=forms.FileInput(attrs={'accept': '.csv'}),
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
        )
