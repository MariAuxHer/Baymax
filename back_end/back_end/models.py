from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Holds Interactions
class Conversation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_accessed = models.DateTimeField(null=True)
    creation_time = models.DateTimeField(null=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # set the times on creation
        if not self.pk: # pk isn't assigned until after creation, so this checks for if a save is a creation
            self.creation_time = timezone.now()
            self.last_accessed = timezone.now()
        super(Conversation, self).save(*args, **kwargs)

    # updates the access time manually
    def update_access_time(self):
        self.last_accessed = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
# Holds prompt and responses
class Interaction(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

    prompt : str =  models.CharField(max_length=1000)
    LLMresponse : str = models.CharField(max_length=1000)

# holds medical service information
class Provider(models.Model):
    name : str = models.CharField(max_length=500)
    location : str = models.CharField(max_length=500)
    # populate more fields or do it in code