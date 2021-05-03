from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    youtubeVideoId = models.CharField(max_length=20)
    caption = models.CharField(max_length=120)
    description = models.TextField(max_length=1000, blank=True, null=True)
    views = models.IntegerField(default=0)
    channel = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_by')
    disliked_by = models.ManyToManyField(User, related_name='disliked_by')

    def __str__(self):
        return self.caption
    

class Subscriber(models.Model):
    channel = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='subscribers')
    def __str__(self):
        return self.channel

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    