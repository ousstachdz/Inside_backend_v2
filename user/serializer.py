from rest_framework import serializers
from django.db.models import Q

from .models import UserApp, UserInformations
from friendship.models import RequestFriendShip


class UserInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformations
        fields = '__all__'


class BasicsInfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = ['id', 'first_name', 'last_name', 'bio', 'photo',]


class UserAppSerializer(serializers.ModelSerializer):
    more_info = UserInformationsSerializer()
    friends = serializers.SerializerMethodField(method_name='get_friends')

    def __init__(self, *args, **kwargs):
        self.authenticated_user_id = kwargs.pop('pk')
        print(self.authenticated_user_id)
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserApp
        fields = ['id', 'first_name', 'last_name', 'bio', 'photo',
                  'photo_cover', 'last_login', 'date_joined', 'email', 'more_info', 'friends',]
        extra_kwargs = {'email': {'read_only': True}}

    def get_friends(self, obj):
        friends = []
        self.authenticated_user_id
        query = (Q(to_user=self.authenticated_user_id) |
                 Q(from_user=self.authenticated_user_id))

        friend_ships_requests = RequestFriendShip.objects.filter(
            query).filter(is_accepted=True)

        for request in friend_ships_requests:
            if (request.from_user.id == self.authenticated_user_id):
                friends.append(request.to_user)
            else:
                friends.append(request.from_user)

        serializer = BasicsInfoUserSerializer(friends, many=True)
        return serializer.data


class SearchUserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.authenticated_user_id = kwargs.pop('pk')
        print(self.authenticated_user_id)
        super().__init__(*args, **kwargs)

    relation = serializers.SerializerMethodField(method_name='get_relation')

    class Meta:
        model = UserApp
        fields = ['id',
                  'first_name',
                  'last_name',
                  'bio',
                  'photo',
                  'relation'
                  ]

    def get_relation(self, obj):
        data = {
            'is_authenticated_user': self.get_is_authenticated_user(obj),
            'is_friend': self.get_is_friend(obj),
            'is_send_request': self.get_is_send_request(obj),
            'is_recieve_request': self.get_is_recieve_request(obj)
        }
        return data

    def get_is_authenticated_user(self, obj):
        if obj.id == self.authenticated_user_id:
            return True
        else:
            return False

    def get_is_friend(self, obj):

        query = (Q(to_user=self.authenticated_user_id, from_user=obj.id) |
                 Q(to_user=obj.id, from_user=self.authenticated_user_id))

        request = RequestFriendShip.objects.filter(
            query).filter(is_accepted=True)
        if request.count() > 0:
            return True
        else:
            return False

    def get_is_recieve_request(self, obj):

        query = Q(to_user=obj.id, from_user=self.authenticated_user_id)
        request = RequestFriendShip.objects.filter(
            query)
        if request.count() > 0:
            return True
        else:
            return False

    def get_is_send_request(self, obj):

        query = Q(to_user=self.authenticated_user_id, from_user=obj.id)
        request = RequestFriendShip.objects.filter(
            query)
        if request.count() > 0:
            return True
        else:
            return False
