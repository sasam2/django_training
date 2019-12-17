# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    author = models.TextField()
    date = models.DateTimeField(auto_now_add=True)