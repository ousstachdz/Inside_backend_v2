from rest_framework import serializers

from .models import UserApp


class UserAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'groups': {
            'write_only': True}, 'user_permissions': {'write_only': True}, }
