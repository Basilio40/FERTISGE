# -*- coding: utf-8 -*-

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from djangosige.configs import DEBUG

app_name = 'base'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('criar_usuario', views.criar_usuario, name='criar_usuario'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns += [
        path('404/', views.handler404),
        path('500/', views.handler500),
    ]
