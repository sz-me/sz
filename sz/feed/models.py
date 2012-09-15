from django.db import models
from django.contrib import auth


# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=1024) #Like a TEXT field
    begin = models.DateField(auto_now_add=True)
    end = models.DateField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    pub_date = models.DateTimeField(auto_now_add=True) #Like a DATETIME field
    user = models.ForeignKey(auth.models.User)
    def __unicode__(self): #Tell it to return as a unicode string (The name of the to-do item) rather than just Object.
        return self.text