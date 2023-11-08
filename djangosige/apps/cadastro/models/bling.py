# -*- coding: utf-8 -*-

from django.db import models

class BlingAccount(models.Model):
    username = models.CharField(null=True, blank=True)
    password = models.CharField(null=True, blank=True)

    api_id = models.CharField(null=True, blank=True)
    api_secret = models.CharField(null=True, blank=True)
    
    class Meta:
        verbose_name = "BlingAccount"
