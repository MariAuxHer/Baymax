from django.http import HttpResponse
from rest_framework import viewsets, permissions
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer
from back_end.models import Conversation, Interaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        filtered_queryset = Conversation.objects.filter(owner = request.user)

        user_conversations_serializer = ConversationSerializer(filtered_queryset, many=True, context={'request': request})
        return Response(user_conversations_serializer.data)
    
    def create(self, request):
        
        new_conversation = Conversation(owner = request.user)
        new_conversation.name = request.data['name']

        new_conversation.save()

        return Response(ConversationSerializer(new_conversation, context={'request': request}).data)
    

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

def index(request):
    return HttpResponse("test")