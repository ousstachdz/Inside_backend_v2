from django.urls import path
from . import views

urlpatterns = [
    path('send_request/', views.send_request, name='send_request'),
    path('accept_request/', views.accept_request, name='accept_request'),
    path('refuse_request/', views.refuse_request, name='refuse_request'),
    path('remove_friend/', views.remove_friend, name='remove_friend'),
    path('get_all_requests/', views.get_all_requests, name='get_all_requests'),
]
