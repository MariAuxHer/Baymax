from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
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
    
    @action(detail=True, methods=['post'], serializer_class=InteractionSerializer)
    def add_interaction(self, request, pk):
        c = get_object_or_404(Conversation, pk=pk)
        i = Interaction.objects.create(owner = request.user, prompt = request.data['prompt'], conversation = c)

        serializer = InteractionSerializer(i, context={'request': request})
        return Response(serializer.data)

    

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        filtered_queryset = Interaction.objects.filter(owner = request.user)
        user_interactions_serializer = InteractionSerializer(filtered_queryset, many=True, context={'request': request})
        return Response(user_interactions_serializer.data)

# default page response
def index(request):
    return HttpResponse("test")