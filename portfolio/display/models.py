# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    #author = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="post_images", blank=True)