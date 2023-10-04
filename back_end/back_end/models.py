from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Holds Interactions
class Conversation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_accessed = models.DateTimeField(null=True)
    creation_time = models.DateTimeField(null=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creation_time = timezone.now()
            self.last_accessed = timezone.now()
        super(Conversation, self).save(*args, **kwargs)

    def update_access_time(self):
        self.last_accessed = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
# Holds prompt and responses
class Interaction(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    prompt : str =  models.CharField(max_length=1000)
    LLMresponse : str = models.CharField(max_length=1000)

# updates the time on the conversation when a new interaction is saved
@receiver(post_save, sender=Interaction)
def update_time_accessed(sender, instance, **kwargs):
    if (instance.conversation):
        instance.conversation.update_access_time()

# holds medical service information
class Provider(models.Model):
    name : str = models.CharField(max_length=500)
    location : str = models.CharField(max_length=500)
    # populate more fields or do it in code