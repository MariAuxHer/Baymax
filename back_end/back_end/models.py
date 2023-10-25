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
        time = timezone.now()
        # set the times on creation
        if not self.pk: # pk isn't assigned until after creation, so this checks for if a save is a creation
            self.creation_time = time
            self.last_accessed = time
        super(Conversation, self).save(*args, **kwargs)

    # updates the access time manually
    def update_access_time(self):
        self.last_accessed = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
# Holds prompt and responses
class Interaction(models.Model):
    creation_time = models.DateTimeField(null = True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

    prompt : str =  models.CharField(max_length=1000, null = True)
    LLMresponse : str = models.CharField(max_length=1000)

    def generate_LLMResponse(self):
        self.LLMresponse = "sample LLMResponse"
        # send self.prompt to the LLM
        # get the response back
        # set equal to the LLM Response
        pass

    def save(self, *args, **kwargs):
        if not self.pk: # pk isn't assigned until after creation, so this checks for if a save is a creation
            self.creation_time = timezone.now()
            if (self.prompt): 
                self.generate_LLMResponse()

        super(Interaction, self).save(*args, **kwargs)


# holds medical service information
# class Provider(models.Model):
#     prov : str = models.CharField(max_length=500) # provider name
#     location : str = models.CharField(max_length=500)
#     m_address : str = models.CharField(max_length=500) # mailing address
#     phone : str = models.CharField(max_length=500)
    
    
    # populate more fields or do it in code