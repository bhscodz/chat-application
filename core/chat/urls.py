from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('add_member/<str:room_name>/',views.add_member_to_room,name='add_member'),
    path('<str:room_name>/',views.room,name='room'),
]
