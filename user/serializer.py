from rest_framework import serializers
from django.db.models import Q

from .models import UserApp, UserInformations
from friendship.models import RequestFriendShip


class UserInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformations
        fields = '__all__'


class UserAppSerializer(serializers.ModelSerializer):
    user_id = ''
    more_info = UserInformationsSerializer()
    friends = serializers.SerializerMethodField(method_name='get_friends')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('pk')
        print(self.user_id)
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserApp
        fields = ['id', 'first_name', 'last_name', 'bio', 'photo',
                  'photo_cover', 'last_login', 'date_joined', 'email', 'more_info', 'friends',]
        extra_kwargs = {'email': {'read_only': True}}

    def get_friends(self, obj):
        friends = []
        authenticated_user_id = self.user_id
        query = Q(Q(to_user=authenticated_user_id) |
                  Q(from_user=authenticated_user_id))

        print(query)
        friend_ships_requests = RequestFriendShip.objects.filter(
            query).filter(is_accepted=True)

        for request in friend_ships_requests:
            if (request.from_user.id == authenticated_user_id):
                friends.append(request.to_user)
            else:
                friends.append(request.from_user)

        serializer = BasicsInfoUserSerializer(friends, many=True)
        return serializer.data


class BasicsInfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = ['id', 'first_name', 'last_name', 'bio', 'photo',]


class SearchUserSerializer(serializers.ModelSerializer):
    request = {}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        print(self.request)
        super().__init__(*args, **kwargs)

    is_authenticated_user = serializers.SerializerMethodField(
        method_name='get_is_authenticated_user')
    is_friend = serializers.SerializerMethodField(method_name='get_is_friend')
    is_send_request = serializers.SerializerMethodField(
        method_name='get_is_send_request')
    is_recieve_request = serializers.SerializerMethodField(
        method_name='get_is_recieve_request')

    class Meta:
        model = UserApp
        fields = ['id',
                  'first_name',
                  'last_name',
                  'bio',
                  'photo',
                  'is_authenticated_user',
                  'is_friend',
                  'is_send_request',
                  'is_recieve_request'
                  ]

    def get_is_authenticated_user(self, obj):
        if obj.id == self.request:
            return True
        else:
            return False

    def get_is_friend(self, obj):
        authenticated_user_id = self.request
        user_id = obj.id
        query = Q(Q(to_user=authenticated_user_id, from_user=user_id) |
                  Q(to_user=user_id, from_user=authenticated_user_id))

        request = RequestFriendShip.objects.filter(
            query).filter(is_accepted=True)
        if request.count() > 0:
            return True
        else:
            return False

    def get_is_send_request(self, obj):
        authenticated_user_id = self.request
        user_id = obj.id

        query = Q(to_user=user_id, from_user=authenticated_user_id)
        request = RequestFriendShip.objects.filter(
            query).filter(is_accepted=True)
        if request.count() > 0:
            return True
        else:
            return False

    def get_is_recieve_request(self, obj):
        authenticated_user_id = self.request
        user_id = obj.id

        query = Q(to_user=authenticated_user_id, from_user=user_id)
        request = RequestFriendShip.objects.filter(
            query).filter(is_accepted=True)
        if request.count() > 0:
            return True
        else:
            return False
