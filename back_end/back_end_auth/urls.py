from django.urls import path
from . import views

urlpatterns = [
    path('csrf', views.CSRF.as_view(), name='api-csrf'),
    path('login', views.LoginView.as_view(), name='api-login'),
    path('logout', views.LogoutView.as_view(), name='api-logout'),
    path('session', views.SessionView.as_view(), name='api-session'),
    path('whoami', views.WhoAmIView.as_view(), name='api-whoami'),
]