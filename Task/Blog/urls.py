from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('users', Users.as_view(), name='userslist'),
    path('users/<username>', UserBlog.as_view(), name='userblog'),
    path('users/<username>/subscribe', Subscribe.as_view(), name='subscribe'),
    path('myblog', MyBlog.as_view(), name='myblog'),
    path('createpost', CreatePost.as_view(), name='newpost'),

]