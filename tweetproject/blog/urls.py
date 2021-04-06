from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('all/', bloglist, name="postlist"),
    path('detail/<int:pk>', blogdetail, name="blogdetail"),
    path('detail/<int:pk>/like', postlike, name="postlike"),
    path('create/', postcreate, name='postcreate'),
    path('delete/<int:pk>', postdelete, name="postdelete"),
    path('update/<int:pk>', postupdate, name="postupdate"),
    path('deletecomment/<int:pk>', deletecomment, name="deletecomment"),
    path('retweet/<int:pk>', postretweet, name="postretweet"),
    path('tweets', personalposts, name="personalposts"),
]
