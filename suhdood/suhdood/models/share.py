# -*- coding: utf-8 -*-
""" share.py
"""
from django.conf import settings
from django.db import models
from suhdood.models.account import Account

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'suhdood.Account')

class ShareManager(models.Manager):
    pass

class Share(models.Model):
    """
    Shared urls between users
    """
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_share', verbose_name=('Sender'))
    receiver = models.ForeignKey(AUTH_USER_MODEL, related_name='received_share', verbose_name=('Receiver'))
    shared_url = models.CharField(('URL'), max_length=255)

    class Meta:
        verbose_name = ('Share')
