from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.relations import SlugRelatedField
from contact.models import Contact, ContactStatus


class ContactSerializer(ModelSerializer):
    status = SlugRelatedField(
        queryset=ContactStatus.objects.all(),
        slug_field='name'
    )
    phone_number = CharField(write_only=True)
    email = CharField(write_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'phone_number',
            'email', 'city', 'status', 'created'
        ]
