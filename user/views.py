from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F

from .serializer import UserAppSerializer
from .models import UserApp


'''
/////// ALERT
This endpoint is just for testing perposes
'''


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def get_fake_data_users(request):
    data = request.data

    serializer = UserAppSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
    return Response(data=serializer.data, status=200)


@api_view()
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        user = UserApp.objects.get(id=request.user.id)
    except:
        return Response(data={'message': 'bad request'}, status=400)
    serializer = UserAppSerializer(user)
    return Response(data=serializer.data, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def search_user(request):
    kw = request.data['kw']
    query = (Q(first_name__contains=kw) | Q(last_name__contains=kw)
             | Q(email__contains=kw))
    try:
        user = UserApp.objects.filter(query)
    except:
        return Response(data={'message': 'bad request'}, status=400)

    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset=user, request=request)
    serializer = UserAppSerializer(page, many=True)
    return Response(data=serializer.data, status=200)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_user_by_id(request, id):
    try:
        user = UserApp.objects.get(id=id)
    except:
        return Response(data={'message': 'bad request'}, status=400)
    serializer = UserAppSerializer(user)
    return Response(data=serializer.data, status=200)
    # return Response(staus=200)
