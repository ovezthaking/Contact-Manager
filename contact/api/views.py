from rest_framework.response import Response
from rest_framework.decorators import api_view
from contact.models import Contact


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
