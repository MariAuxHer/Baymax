from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import logout

# database
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer, MinimalConversationSerializer
from back_end.models import Conversation, Interaction, CustomUser

def index(request):

    if request.user.is_authenticated:
        conversations = Conversation.objects.filter(owner = request.user)

        print(conversations)
        
        try:
            interaction_set = Interaction.objects.filter(conversation = conversations[0])
            context = {
                "interaction_set": interaction_set
            }

            print(interaction_set)
        except:
            context = {}
    else:
        return redirect('/login')

    return render(request, "back_end/index.html", context = context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, "back_end/profile.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, "back_end/login.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, "back_end/signup.html")

def about(request):
    return render(request, "back_end/about.html")

def test(request):
    return render(request, "back_end/test.html")

def search(request):
    return render(request, "back_end/search.html")

def signout(request):
    logout(request)
    return redirect('/login')

def changeprofile(request):
    return render(request, "back_end/changeprofile.html")