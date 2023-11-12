from django.contrib import admin

from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'city', 'state', 'zipcode')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(Conversation)
admin.site.register(CustomUser)