from django.urls import path
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


urlpatterns = [
    path('set_fake_data_users/', views.get_fake_data_users,
         name='get_fake_data_users'),
    path('set_fake_data/', views.get_fake_data,
         name='get_fake_data'),

    path('api/user/get_authenticated_user/',
         views.get_authenticated_user, name='get_authenticated_user'),
    path('api/user/search/', views.search_user, name='search_user'),
    path('api/user/get_user_by_id/<str:id>',
         views.get_user_by_id, name='get_user'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
