from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm

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


def createContact(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'contact/contact_form.html', context)
