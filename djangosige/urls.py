# -*- coding: utf-8 -*-

from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from .configs.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangosige.apps.base.urls')),
    path('login/', include('djangosige.apps.login.urls')),
    path('cadastro/', include('djangosige.apps.cadastro.urls')),
    path('fiscal/', include('djangosige.apps.fiscal.urls')),
    path('vendas/', include('djangosige.apps.vendas.urls')),
    path('compras/', include('djangosige.apps.compras.urls')),
    path('financeiro/', include('djangosige.apps.financeiro.urls')),
    path('estoque/', include('djangosige.apps.estoque.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
