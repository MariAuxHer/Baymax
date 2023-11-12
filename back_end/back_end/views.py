from django.shortcuts import render

# database
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer, MinimalConversationSerializer
from back_end.models import Conversation, Interaction, CustomUser

def index(request):
    return render(request, "back_end/index.html")

def profile(request):
    return render(request, "back_end/profile.html")

def login(request):
    return render(request, "back_end/login.html")

def signup(request):
    return render(request, "back_end/signup.html")

def about(request):
    return render(request, "back_end/about.html")

def test(request):
    return render(request, "back_end/test.html")