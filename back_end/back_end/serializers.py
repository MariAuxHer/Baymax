from back_end.models import Conversation, Interaction
from rest_framework import serializers
from django.contrib.auth.models import User

class InteractionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'
        read_only_fields = ['LLMresponse', 'owner', 'conversation']

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    interaction_set = InteractionSerializer(many=True, required=False)

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'last_accessed', 'creation_time', 'interaction_set']

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'is_staff']
        read_only_fields = ['url, groups', 'is_staff']



