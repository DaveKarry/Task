from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        return render(self.request, 'users/index.html')
