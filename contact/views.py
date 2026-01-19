import csv
import io

from django.shortcuts import render, redirect
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse

from .models import Contact, ContactStatus
from .forms import ContactForm, ImportContactsForm


# Create your views here.


def index(request):
    sort_param = request.GET.get('sort_by', 'last_name')
    order = request.GET.get('order', 'asc')
    query = request.GET.get('q', '')

    sort_options = {
        'last_name': 'last_name',
        'created': 'created',
    }

    sort_direction = ''
    if order == 'desc':
        sort_direction = '-'

    sort_field = f'{sort_direction}{sort_param}'
    contacts = Contact.objects.all()

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )

    contacts = contacts.order_by(sort_field)

    contacts_count = contacts.count()
    context = {
        'contacts': contacts,
        'contacts_count': contacts_count,
        'active_sort': sort_param if sort_param in sort_options else 'created',
        'order': order,
        'query': query,
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


def importContacts(request):
    form = ImportContactsForm()

    if request.method == 'POST':
        form = ImportContactsForm(request.POST, request.FILES)

        if form.is_valid():
            data = request.FILES['file'].read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(data))

            created = 0
            skipped = 0

            # if not file.name.endswith('.csv'):
            #     messages.error(request, 'CSV files only')
            #     return redirect('import-contacts')

            # No problems - commit to the database, othervise roll back
            with transaction.atomic():
                for row in reader:
                    status, _ = ContactStatus.objects.get_or_create(
                        name=row['status']
                    )

                    contact, is_created = Contact.objects.get_or_create(
                        email=row['email'],
                        defaults={
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'phone_number': row['phone_number'],
                            'city': row['city'],
                            'status': status,
                        }
                    )

                    if is_created:
                        created += 1
                    else:
                        skipped += 1

            messages.success(
                request,
                f'Imported: {created}, skipped (duplicates): {skipped}',
                extra_tags='bg-green-100 text-green-800'
            )

            print(messages)
            return redirect('home')

    context = {'form': form}
    return render(request, 'contact/import_form.html', context)


def exportContacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'first_name',
        'last_name',
        'phone_number',
        'email',
        'city',
        'status'
    ])

    contacts = Contact.objects.all().select_related('status')

    for contact in contacts:
        writer.writerow([
            contact.first_name,
            contact.last_name,
            contact.phone_number,
            contact.email,
            contact.city,
            contact.status.name
        ])

    return response
