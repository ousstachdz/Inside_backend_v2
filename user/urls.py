from django.urls import path

from . import views


urlpatterns = [

    path('get_authenticated_user/', views.get_authenticated_user,
         name='get_authenticated_user'),
    path('search/', views.search_user, name='search_user'),
    path('get_user_by_id/<str:id>', views.get_user_by_id, name='get_user'),

]

#     path('set_fake_data_users/', views.get_fake_data_users,
#          name='get_fake_data_users'),
#     path('set_fake_data/', views.get_fake_data,
#          name='get_fake_data'),
