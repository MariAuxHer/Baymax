"""
URL configuration for back_end project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
import back_end_auth.urls
from rest_framework import routers

api_router = routers.DefaultRouter()

api_router.register(r'conversations', views.ConversationViewSet, basename = 'conversation')
api_router.register(r'interactions', views.InteractionViewSet, basename = 'interaction')    
api_router.register(r'users', views.UserViewSet, basename = 'user')
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(back_end_auth.urls)),
    path('api/', include(api_router.urls)),
    path('', views.index)
]
