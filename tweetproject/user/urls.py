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
    path('search/', search, name="search"),
    path('viewfollowing/<int:pk>', viewfollowing, name="viewfollowing"),
    path('viewfollowers', viewfollowers, name="viewfollowers"),
    path('accountdelete', accountdelete, name="accountdelete"),
    path('passwordupdate', passwordupdate, name="passwordupdate"),
    # path('resetpassword', passwordreset, name="passwordreset"),
]