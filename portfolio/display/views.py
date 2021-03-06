# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse

from .forms import SignupForm, PosteditForm

from .models import Post

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib import auth
import json

# Import Datetime
from datetime import datetime

from django.core import serializers

from django.core.files.storage import FileSystemStorage

# Create your views here.
from django.http import HttpResponse

def post_view(request):
    lastPost = request.GET.get('lastPost')
    if lastPost:
        posts = list(Post.objects.select_related('author').filter(id__lt=lastPost).order_by('-date')[:2].values())
        for p in posts:
            author_id = p.pop('author_id')
            p['author'] = User.objects.get(id=author_id).username
            date = p.pop('date')
            p['date'] = date.strftime("%Y-%m-%d %H:%M:%S")
        resp = json.dumps(posts)
        #print resp
        #data = serializers.serialize("json", posts)
        return JsonResponse(resp, safe=False)

    # request.session['foo'] = 'bar'
    post = Post.objects.select_related('author').order_by('-date')[:2]
    print 'posts ', post[0].author
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







