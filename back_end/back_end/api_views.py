from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from back_end.serializers import ConversationSerializer, UserSerializer, InteractionSerializer, MinimalConversationSerializer
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator

from back_end.models import Conversation, Interaction, CustomUser
#from django.contrib.auth.models import User 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset =  CustomUser.objects.all().order_by('-date_joined')
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
    
    # Allow the list to have a custom HTTP Header that can specify to have interaction sets returned or not
    def list(self, request):
        serializer = ConversationSerializer

        try:
            show_interactions = request.META.get('HTTP_X_SHOWINTS')
            if (show_interactions and show_interactions.lower() == "false"):
                print("changing to minimal")
                serializer = MinimalConversationSerializer
        finally:
            return Response(serializer(self.get_queryset(), many=True, context = {'request': request}).data)
    
    # auto associate the owner with the newly created conversation
    def create(self, request):
        new_conversation = Conversation.objects.create(owner = request.user, name = request.data['name'])
        return Response(ConversationSerializer(new_conversation, context={'request': request}).data, status=status.HTTP_201_CREATED)
    
    # allow API user to add new interactions to Conversation Instances
    @action(detail=True, methods=['post', 'get'], serializer_class=InteractionSerializer)
    def interactions(self, request, pk):
        # add the ability to post a new prompt
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
    
    def update(self, request, pk=None):
        if (not pk): 
            return Response({"detail": "PUT failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        interaction = get_object_or_404(Interaction, pk=pk)
        new_prompt = request.data['prompt']
        if (new_prompt):
            interaction.prompt = new_prompt 

        interaction.generate_LLMResponse()
        interaction.save()

        return Response(InteractionSerializer(interaction, context = {'request': request}).data)
   
class CreateUser(APIView):
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        city = request.data['city']
        state = request.data['state']
        zipcode = request.data['zipcode']

        if (not username or not password or not email or not city or not state or not zipcode):
            return Response({'detail' : 'Missing one or more of the following fields: username, password, email, city, state, zipcode.'}, status = status.HTTP_400_BAD_REQUEST)
        

        # check username
        # UnicodeUsernameValidator()
        username_validator = ASCIIUsernameValidator() 
        try:
            username_validator(username)
        except ValidationError:
            return Response({'detail': 'Invalid username. ' + username_validator.message}, status = status.HTTP_400_BAD_REQUEST)
        
        # check if username is taken
        if (CustomUser.objects.filter(username = username).count() != 0):
            return Response({'detail': 'Username already taken.'}, status = status.HTTP_409_CONFLICT)
        
        # validate password
        try:
            validate_password(password)
        except ValidationError:
            help_text = " ".join(password_validators_help_texts())
            return Response({'detail': help_text}, status = status.HTTP_400_BAD_REQUEST)

        # validate email
        try:
            validate_email(email)

        except ValidationError:
            return Response({'detail': 'Invalid email.'}, status = status.HTTP_400_BAD_REQUEST)
        
        # MAYBE LATER VALIDATE CITY, STATE, AND ZIP CODE (like whether the state/city, zip code exists or not in the US)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # create user and set details
        user = CustomUser.objects.create(username = username, email = email, city=city, state=state, zipcode=zipcode)
        user.set_password(password)
        user.save()

        # return the new serialized user
        return Response(UserSerializer(user, context = {'request': request}).data, status = status.HTTP_200_OK)

    def get(self, request, format=None):
        return Response({'detail': 'There is no GET here.'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
# default page response
class IndexView(APIView):
    def get(self, request, format=None):
        return Response({"detail": "This page doesn't have anything right now, but this message is intended."})

