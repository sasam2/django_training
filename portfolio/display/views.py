# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse

from .forms import SignupForm, PosteditForm

from .models import Post

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib import auth

from django.core import serializers

from django.core.files.storage import FileSystemStorage

# Create your views here.
from django.http import HttpResponse

def post_view(request):
    first_post = request.GET.get('lastPost')
    print first_post
    if first_post:
        posts = Post.objects.filter(id__gt=first_post).order_by('-date')[:2]
        data = serializers.serialize("json", posts)
        return JsonResponse(data, safe=False)

    # request.session['foo'] = 'bar'
    post = Post.objects.order_by('-date')[:2]
    return render(request, 'post_view.html', {'post': post})

def post_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/portfolio/signin/')

    if request.method == 'POST':
        form = PosteditForm(request.POST)
        photo = request.FILES['image']
        #fs=FileSystemStorage()
        #filename = fs.save(photo.name, photo)
        form.is_valid()
        p = Post(title=form.cleaned_data['title'],
                 content=form.cleaned_data['content'],
                 author=request.user,
                 photo=request.FILES['image'])
        p.save()

        # redirect to a new URL:
        return HttpResponseRedirect('/portfolio/post_view/')

    # if a GET (or any other method) we'll create a blank form
    form = PosteditForm()
    return render(request, 'post_create.html', {'form': form, 'user': request.user})

def post_delete(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/portfolio/signin/')

    if request.method == 'POST':
        p = Post.objects.get(id = request.POST['post_id'])
        if p.author == request.user:
            p.delete()

    return HttpResponseRedirect('/portfolio/post_view/')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/portfolio/signout')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(form.cleaned_data['username'], 'no@email.com', form.cleaned_data['password'])
            u.save()
            return HttpResponseRedirect('/portfolio/signin/')

    # if a GET (or any other method) we'll create a blank form
    form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/portfolio/signout')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None :
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                return HttpResponseRedirect('/portfolio/post_view/')

    # if a GET (or any other method) we'll create a blank form
    form = SignupForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/portfolio/signin')

    if request.method == 'POST':
        auth.logout(request)
        return HttpResponseRedirect('/portfolio/post_view/')

    return render(request, 'signout.html')







