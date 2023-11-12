from django.shortcuts import render

# database
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer, MinimalConversationSerializer
from back_end.models import Conversation, Interaction, CustomUser

def index(request):

    if request.user.is_authenticated:
        conversations = Conversation.objects.filter(owner = request.user)

        print(conversations)

        interaction_set = Interaction.objects.filter(conversation = conversations[0])
        context = {
            "interaction_set": interaction_set
        }

        print(interaction_set)
    else:
        context = {}

    return render(request, "back_end/index.html", context = context)

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