from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from Blog.forms import PostForm
from Blog.models import Post, NewUser


class Index(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(
                author=self.request.user
            ).order_by('-posted_date')
            return render(self.request, 'blog/index.html', {'posts': posts})
        else:
            message = "Войдите что-бы просмотреть свои посты!"
            return render(self.request, 'blog/index.html', {'message': message})


class Users(View):
    def get(self, *args, **kwargs):
        users = NewUser.objects.all()
        return render(self.request, "blog/users.html", {'users': users})


class MyBlog(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(
                author=self.request.user
            ).order_by('-posted_date')
            form = PostForm()
            context = {'form': form, 'posts': posts}
            return render(self.request, "blog/myblog.html", context)
        else:
            message = "Войдите что-бы просмотреть свои посты!"
            return render(self.request, 'blog/myblog.html', {'message': message})

    def post(self, *args, **kwargs):
        form = PostForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            currentUser = self.request.user
            post.author = currentUser
            post.save()

            users = NewUser.objects.filter(subscribers=currentUser)
            emails = []
            for u in users:
                emails.append(u.email)
            send_mail(
                f"New Post from {currentUser}!",
                f"hello! Your Fav have posted new post http://127.0.0.1:8000/post/{post.id}",
                "davekarry1337@gmail.com",
                emails
            )
            print(users)
            return redirect('myblog')
        else:
            return HttpResponseRedirect('createtovar')


""""

Этот метод аналогичен верхнему, так-что я просто работал с верхним
"""


class CreatePost(View):
    def get(self, *args, **kwargs):
        form = PostForm()
        context = {'form': form}
        return render(self.request, 'blog/createpost.html', context)

    def post(self, *args, **kwargs):
        messages = False
        form = PostForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()

            return redirect('myblog')
        else:
            messages.info(self.request, 'Какая-то ошибка! Прверьте поля или попробуйте снова!')
            return HttpResponseRedirect('createpost')


class UserBlog(View):
    def get(self, *args, **kwargs):
        targetUser = get_object_or_404(NewUser, username=kwargs['username'])
        posts = Post.objects.filter(
            author=targetUser
        ).order_by('-posted_date')
        if self.request.user.is_authenticated:
            currentUser = self.request.user
            if targetUser in currentUser.subscribers.all():
                isSub = "sub"
            else:
                isSub = "unsub"
        else:
            isSub = "notAuth"
        context = {'user': targetUser, 'posts': posts, 'isSub': isSub}
        return render(self.request, 'blog/userblog.html', context)


class Subscribe(View):
    def get(self, *args, **kwargs):
        targetUser = get_object_or_404(NewUser, username=kwargs['username'])
        currentUser = self.request.user
        currentUser.subscribers.add(targetUser)
        posts = Post.objects.filter(
            author=targetUser
        ).order_by('-posted_date')
        isSub = "sub"
        context = {'user': targetUser, 'posts': posts, 'isSub': isSub}
        return render(self.request, 'blog/userblog.html', context)


class UnSubscribe(View):
    def get(self, *args, **kwargs):
        targetUser = get_object_or_404(NewUser, username=kwargs['username'])
        currentUser = self.request.user
        currentUser.subscribers.remove(targetUser)
        posts = Post.objects.filter(
            author=targetUser
        ).order_by('-posted_date')
        isSub = "unsub"
        context = {'user': targetUser, 'posts': posts, 'isSub': isSub}
        return render(self.request, 'blog/userblog.html', context)


class MyNews(View):
    def get(self, *args, **kwargs):
        currentUser = self.request.user
        posts = Post.objects.none()
        for person in currentUser.subscribers.all():
            posts |= Post.objects.filter(
                author=person
            ).order_by('-posted_date')
        context = {'posts': posts}
        return render(self.request, 'blog/mynews.html', context)


class GetPost(View):
    def get(self, *args, **kwargs):
        targetPost = get_object_or_404(Post, id=kwargs['id'])
        return render(self.request, 'blog/post.html', {"targetPost": targetPost})


class SetSeen(View):
    def get(self, *args, **kwargs):
        targetPost = get_object_or_404(Post, id=kwargs['id'])
        currentUser = self.request.user
        if targetPost in currentUser.seen_posts.all():
            isSeen = False
            print("1")
            currentUser.seen_posts.remove(targetPost)
        else:
            isSeen = True
            print("2")
            currentUser.seen_posts.add(targetPost)
        context = {"targetPost": targetPost, 'isSeen': isSeen}
        return render(self.request, 'blog/post.html', context)

