from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer
from rest_framework.views import APIView

from back_end.models import Conversation, Interaction
from django.contrib.auth.models import User 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import status

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

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if (not created):
                return Response({'detail': 'Failed token creation.'})
            
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
def logout(request):
    logout(request)