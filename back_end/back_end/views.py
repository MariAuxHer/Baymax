from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer

from back_end.models import Conversation, Interaction
from django.contrib.auth.models import User 
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Conversations to be viewed or edited.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Only allow the user to conrol their own Conversations
    def get_queryset(self):
        return Conversation.objects.filter(owner = self.request.user)
    
    # auto associate the owner with the newly created conversation
    def create(self, request):
        new_conversation = Conversation(owner = request.user)
        new_conversation.name = request.data['name']
        new_conversation.save()
        return Response(ConversationSerializer(new_conversation, context={'request': request}).data)
    
    # allow API user to add new interactions to Conversation Instances
    @action(detail=True, methods=['post'], serializer_class=InteractionSerializer)
    def add_interaction(self, request, pk):
        c = get_object_or_404(Conversation, pk=pk)
        i = Interaction.objects.create(owner = request.user, prompt = request.data['prompt'], conversation = c)

        serializer = InteractionSerializer(i, context={'request': request})
        return Response(serializer.data)
    
# default page response
def index(request):
    return HttpResponse("test")

