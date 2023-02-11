from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import UserAppSerializer
from .models import UserApp


@api_view()
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        user = UserApp.objects.get(id=request.user.id)
    except:
        return Response(data={'message': 'bad request'}, status=400)
    serializer = UserAppSerializer(user)
    return Response(data=serializer.data, status=200)

    #

# Create your views here.
