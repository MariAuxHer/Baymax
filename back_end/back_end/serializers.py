from back_end.models import Conversation, Interaction, CustomUser
from rest_framework import serializers
#from django.contrib.auth.models import User

class InteractionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interaction
        fields = ['url', 'LLMresponse', 'owner', 'conversation', 'prompt', 'creation_time']
        read_only_fields = ['url', 'LLMresponse', 'owner', 'conversation', 'creation_time']

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    interaction_set = serializers.SerializerMethodField('get_interaction_set')

    class Meta:
        model = Conversation
        fields = ['url', 'owner', 'last_accessed', 'creation_time', 'interaction_set', 'name']
        read_only_fields = ['url', 'owner', 'last_accessed', 'creation_time', 'interaction_set']

    def get_interaction_set(self, obj):
        serializer_context = {'request': self.context.get('request') }
        interactions = Interaction.objects.filter(conversation = obj).order_by('-creation_time')
        return InteractionSerializer(interactions, context = serializer_context, many = True).data

"""
By specifying these fields in the fields attribute, you're telling DRF to only consider these fields when working with the serializer and to ignore any other fields present in the model.
"""

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'email', 'city', 'state', 'zipcode', 'groups', 'is_staff']
        read_only_fields = ['url', 'groups', 'is_staff']



