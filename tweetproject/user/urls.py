from django.urls import path
from .views import *

urlpatterns = [
    path('createuser', createuser, name="createuser"),
    path('loginuser', loginuser, name="loginuser"),
    path('logoutuser', logoutuser, name="logoutuser"),
    path('detailuser/<int:pk>', detailuser, name="detailuser"),
    path('allusers', allusers, name="allusers"),
    path('followuser/<int:pk>', followuser, name="followuser"),
    path('whotofollow', whotofollow, name="whotofollow"),
    path('updateprofile', updateprofile, name="updateprofile"),
]