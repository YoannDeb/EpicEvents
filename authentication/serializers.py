from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import CustomUser, Client


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer is unused for now.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'date_created', 'date_updated']


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation, unused for now.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'password']

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.
        Apparently necessary with custom user.
        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def validate_email(self, value: str) -> str:
        """
        Overload of validate_email method, converting email and
        checking existence of the email in the database EXCEPT for current user.
        Necessary cause by default for an update, if the mail was the same, the user wasn't updated.
        """
        email = value.lower()
        if self.instance and CustomUser.objects.exclude(pk=self.instance.pk).filter(email=value):
            raise serializers.ValidationError('A user with this email already exists.')
        return email

    def validate_first_name(self, value: str) -> str:
        """
        Overload of validate_first_name method, capitalizing first name.
        """
        return value.capitalize()

    def validate_last_name(self, value: str) -> str:
        """
        Overload of validate_last_name method, capitalizing last name.
        """
        return value.capitalize()


class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer, with sales contact info added as read_only fields.
    """
    sales_contact_first_name = serializers.CharField(read_only=True, source='sales_contact.first_name')
    sales_contact_last_name = serializers.CharField(read_only=True, source='sales_contact.last_name')
    sales_contact_email = serializers.CharField(read_only=True, source='sales_contact.email')

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'date_created', 'date_updated',
                  'company_name', 'sales_contact', 'sales_contact_first_name', 'sales_contact_last_name',
                  'sales_contact_email']
