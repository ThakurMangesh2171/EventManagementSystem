from rest_framework import serializers
from .models import Event,CustomUser


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'organizer']

    def validate_title(self, value):
        """
        Validate the title field.
        """
        if not value:
            raise serializers.ValidationError("Title is mandatory and cannot be null.")
        elif len(value) > 20:
            raise serializers.ValidationError("Title should not be more than 20 characters.")
        return value
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'password',
            'last_login',
            'is_superuser',
            'username',
            'first_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'user_id',
            'last_name',
            'phone_number',
            'email_id',
            'address',
        ]