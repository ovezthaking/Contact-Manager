from rest_framework.response import Response
from rest_framework.decorators import api_view
from contact.models import Contact, ContactStatus
from .serializers import ContactSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/contacts',
        'POST /api/contacts/',
        'PUT /api/contacts/{id}/',
        'DELETE /api/contacts/{id}/'
    ]

    return Response(routes)


@api_view(['GET'])
def getContacts(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)
