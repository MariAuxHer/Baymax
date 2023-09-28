from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# User Chats
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_accessed = models.DateTimeField()
    name = models.CharField(max_length=100)

    def update_access_time(self):
        self.last_accessed = timezone.now()
        pass

class Interaction(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    prompt : str = None
    LLMresponse : str = None

# medical service information

class Provider(models.Model):
    name : str
    location : str
    # populate more fields or do it in code