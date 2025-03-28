"""EMR_STATS_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

import facilities

urlpatterns = [
    path('admin/', admin.site.urls),
    path('facilities/', include('facilities.urls')),
    path('districts/', include('districts.urls')),
    path('zones/', include('zones.urls')),
    path('encounters/', include('encounters.urls')),
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),
    path('databases/', include('databases.urls')),
    path('vpn/', include('vpn.urls')),    
    path('devices/', include('devices.urls')),    
    path('trackusers/', include('trackusers.urls')),   
    path('update_password/', include('change_password.urls')),   
    path('rest_password/', include('rest_password.urls')),   
]
