"""ecommers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import  include
from django.conf import settings #указывают джанго необходимые пути для статических файлов 
from django.conf.urls.static import static #указывают джанго необходимые пути для статических файлов 

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'^', include('shop.urls')),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #когда находимся в режими локальной разработки наши пути к сатическим файлам находятся по этому адресу , в продакшени по другому адресу 
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   #когда находимся в режими локальной разработки наши пути к сатическим файлам находятся по этому адресу , в продакшени по другому адресу 