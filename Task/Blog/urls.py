from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('users', Users.as_view(), name='userslist'),
    path('users/<username>', UserBlog.as_view(), name='userblog'),
    path('users/<username>/subscribe', Subscribe.as_view(), name='subscribe'),
    path('users/<username>/unsubscribe', UnSubscribe.as_view(), name='unsubscribe'),
    path('myblog', MyBlog.as_view(), name='myblog'),
    path('mynews', MyNews.as_view(), name='mynews'),
    path('createpost', CreatePost.as_view(), name='newpost'),

]