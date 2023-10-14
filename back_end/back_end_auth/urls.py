from django.urls import path
from . import views

urlpatterns = [
    path('csrf', views.csrfView.as_view(), name='api-csrf'),
    path('login', views.LoginView.as_view(), name='api-login'),
    path('logout', views.logout_view, name='api-logout'),
    path('session', views.SessionView.as_view(), name='api-session'),
    path('whoami', views.WhoAmIView.as_view(), name='api-whoami'),
]