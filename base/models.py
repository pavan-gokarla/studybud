from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)  # <--- Changed to DateTimeField
    created = models.DateTimeField(auto_now_add=True)  # <--- Changed to DateTimeField

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self) -> str:
        return self.name



class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)  # <--- Changed to DateTimeField
    created = models.DateTimeField(auto_now_add=True)  # <--- Changed to DateTimeField

    def __str__(self) -> str:
        return self.body[0:50]