from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm

# Create your views here.


def index(request):
    sort_param = request.GET.get('sort_by', 'last_name')
    order = request.GET.get('order', 'asc')
    sort_options = {
        'last_name': 'last_name',
        'created': 'created',
    }
    sort_direction = ''
    if order == 'desc':
        sort_direction = '-'

    sort_field = f'{sort_direction}{sort_param}'
    contacts = Contact.objects.all().order_by(sort_field)

    contacts_count = contacts.count()
    context = {
        'contacts': contacts,
        'contacts_count': contacts_count,
        'active_sort': sort_param if sort_param in sort_options else 'created',
        'order': order
    }
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


def updateContact(request, pk):
    contact = Contact.objects.get(id=pk)
    form = ContactForm(instance=contact)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect(f'/contact/{pk}')

    context = {'form': form}
    return render(request, 'contact/contact_form.html', context)


def deleteContact(request, pk):
    contact = Contact.objects.get(id=pk)

    if request.method == 'POST':
        contact.delete()
        return redirect('home')

    context = {'contact': contact}
    return render(request, 'contact/delete.html', context)
