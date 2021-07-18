from django.contrib import admin
from Blog.models import Post, NewUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

admin.site.register(Post)
admin.site.register(NewUser)

