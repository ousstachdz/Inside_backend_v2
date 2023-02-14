from rest_framework import serializers

from .models import RequestFriendShip
from user.models import UserApp


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserApp
        fields = ['id',
                  'first_name',
                  'last_name',
                  'bio',
                  'photo',
                  ]
