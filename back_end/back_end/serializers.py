from back_end.models import Conversation, Interaction
from rest_framework import serializers
from django.contrib.auth.models import User


# class ProfileSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'


class InteractionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    interaction_set = InteractionSerializer(many=True, required=False)

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['owner', 'last_accessed', 'creation_time']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    conversation_set = ConversationSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'conversation_set']
