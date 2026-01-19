from rest_framework.response import Response
from rest_framework.decorators import api_view
from contact.models import Contact
from .serializers import ContactSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/contacts',
        'GET /api/contacts/{id}/',
        'POST /api/contacts/',
        'PUT /api/contacts/{id}/',
        'DELETE /api/contacts/{id}/'
    ]

    return Response(routes)


@api_view(['GET', 'POST'])
def contactsView(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def contactView(request, pk):
    contact = Contact.objects.get(id=pk)

    if request.method == 'GET':
        serializer = ContactSerializer(contact, many=False)

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        contact.delete()
        return Response({'message': 'Contact deleted'}, status=204)
