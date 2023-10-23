from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer

from back_end.models import Conversation, Interaction
from django.contrib.auth.models import User 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Conversations to be viewed or edited.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Only allow the user to conrol their own Conversations
    def get_queryset(self):
        return Conversation.objects.filter(owner = self.request.user).order_by('-creation_time')
    
    # auto associate the owner with the newly created conversation
    def create(self, request):
        new_conversation = Conversation.objects.create(owner = request.user, name = request.data['name'])
        return Response(ConversationSerializer(new_conversation, context={'request': request}).data, status=status.HTTP_201_CREATED)
    
    # allow API user to add new interactions to Conversation Instances
    @action(detail=True, methods=['post', 'get'], serializer_class=InteractionSerializer)
    def interactions(self, request, pk):
        if (request.method == "POST"):
            if (not pk): return Response({"detail": "Missing PK."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            c = get_object_or_404(Conversation, pk=pk)
            i = Interaction.objects.create(owner = request.user, prompt = request.data['prompt'], conversation = c) 
            serializer = InteractionSerializer(i, context={'request': request})
            return Response(serializer.data)

        # perhaps redundant since this information can be gotten from the general Conversation View Set
        if (request.method == "GET"):
            c = get_object_or_404(Conversation, pk=pk)
            interactions = Interaction.objects.filter(conversation = c).order_by("-creation_time")
            return Response(InteractionSerializer(interactions, context={'request': request}, many=True).data)

        return Response({"detail": "Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        if (not pk): 
            return Response({"detail": "Deletion Failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        Conversation.objects.get(pk=pk).delete()
        return Response({"detail": "Conversation successfully removed."}, status=status.HTTP_200_OK)

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Interaction.objects.filter(owner = self.request.user).order_by('-creation_time')
    
    def destroy(self, request, pk=None):
        if (not pk): 
            return Response({"detail": "Deletion Failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        Interaction.objects.get(pk=pk).delete()
        return Response({"detail": "Conversation successfully removed."}, status=status.HTTP_200_OK)
   
# default page response
def index(request):
    return Response({"detail": "This page doesn't have anything right now, but this message is intended."})

