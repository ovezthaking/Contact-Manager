from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField
from contact.models import Contact, ContactStatus


class ContactSerializer(ModelSerializer):
    status = SlugRelatedField(
        queryset=ContactStatus.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'city', 'status', 'created']
