# -*- coding: utf-8 -*-
""" url.py
"""
from django.conf import settings
from django.db import models
import hashlib
import uuid

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'suhdood.Account')

class UrlManager(models.Manager):
    def create_url(self, url):
        hash_object = hashlib.md5(url.encode('utf-8'))
        url = self.create(
            hashed_url = hash_object.hexdigest(),
            url_string = url
        )
        return url

class Url(models.Model):
    """
    Model for URL
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hashed_url = models.CharField(max_length=500)
    url_string = models.URLField(max_length=500)

    objects = UrlManager()

    class Meta:
        verbose_name = ('Url')

    def hash_url(self, url):
        hash_object = hashlib.md5(url.encode('utf-8'))
        return hash_object.hexdigest()

    def __str__(self):
        return self.url_string