# -*- coding: utf-8 -*-

from django.db import models

class BlingAccount(models.Model):
    username = models.CharField(max_length=24, null=True, blank=True)
    password = models.CharField(max_length=24, null=True, blank=True)

    api_id = models.CharField(max_length=45, null=True, blank=True)
    api_secret = models.CharField(max_length=65, null=True, blank=True)
    
    token = models.CharField(max_length=65, null=True, blank=True)
    token_refresh = models.CharField(max_length=65, null=True, blank=True)
    
    token_vality = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "BlingAccount"
