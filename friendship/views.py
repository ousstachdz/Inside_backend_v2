from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import RequestFriendShip
from .serializers import FriendRequestSerializer
from user.models import UserApp


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request):
    from_user = UserApp.objects.get(id=request.user.id)
    to_user = UserApp.objects.get(id=request.data['id'])
    request_friend_ship = RequestFriendShip.objects.create(
        from_user=from_user, to_user=to_user)
    request_friend_ship.save()
    return Response(status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request):
    to_user = UserApp.objects.get(id=request.user.id)
    from_user = UserApp.objects.get(id=request.data['id'])
    request_friend_ship = RequestFriendShip.objects.get(
        from_user=from_user, to_user=to_user)
    request_friend_ship.is_accepted = True
    request_friend_ship.save()
    return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refuse_request(request):
    from_user = UserApp.objects.get(id=request.user.id)
    to_user = UserApp.objects.get(id=request.data['id'])
    request_friend_ship = RequestFriendShip.objects.get(
        from_user=from_user, to_user=to_user)
    request_friend_ship.is_rejected = True
    request_friend_ship.save()
    return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_friend(request):
    authenticated_user = UserApp.objects.get(id=request.user.id)
    friend = UserApp.objects.get(id=request.data['id'])

    query = Q(from_user=authenticated_user, to_user=friend) | Q(
        from_user=friend, to_user=authenticated_user)
    request_friend_ship = RequestFriendShip.objects.get(query)
    request_friend_ship.delete()
    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_requests(request):
    authenticated_user = UserApp.objects.get(id=request.user.id)
    friendship_requests = RequestFriendShip.objects.all().filter(
        to_user=authenticated_user, is_accepted=False)
    users = []
    for friendship_request in friendship_requests:
        users.append(UserApp.objects.get(id=friendship_request.from_user.id))

    serializer = FriendRequestSerializer(users, many=True)
    return Response(serializer.data, status=200)
