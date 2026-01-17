from django.shortcuts import render
from .models import Contact

# Create your views here.


def index(request):
    contacts = Contact.objects.all()

    contacts_count = contacts.count()
    context = {'contacts': contacts, 'contacts_count': contacts_count}
    return render(request, 'contact/index.html', context)


def contact(request, pk):
    contact = Contact.objects.get(id=pk)
    context = {'contact': contact}
    return render(request, 'contact/contact.html', context)
