from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseBadRequest

from django.contrib.auth import logout

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods

# database
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer, MinimalConversationSerializer
from back_end.models import Conversation, Interaction, CustomUser, Doctor

import json

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

def signout(request):
    logout(request)
    return redirect('/login')

def changeprofile(request):
    return render(request, "back_end/changeprofile.html")

@csrf_protect
def search(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_city = data['city'].capitalize()  # Capitalize the city name as stored in the database
            selected_specialization = data['specialization']

            # Filter doctors by city (case-insensitive) and specialization
            doctors = Doctor.objects.filter(
                m_address__icontains=selected_city, 
                specialty__icontains=selected_specialization
            )

            # Serialize the data into a list of dictionaries
            doctor_data = [
                {"name": doctor.name, "address": doctor.m_address, "specialty": doctor.specialty, "phone": doctor.phone_number}
                for doctor in doctors
            ]

            # Return the serialized data as JSON
            return JsonResponse(doctor_data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # If not a POST request, just render the search page
    return render(request, "back_end/search.html")
