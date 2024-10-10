from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create token auth for new users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# MemeTemplate Model
class MemeTemplate(models.Model):
    name = models.CharField(max_length=100)  
    image_url = models.URLField()  
    default_top_text = models.CharField(max_length=100, blank=True) 
    default_bottom_text = models.CharField(max_length=100, blank=True)  

    def __str__(self):
        return self.name

# Meme Model
class Meme(models.Model):
    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE)  
    top_text = models.CharField(max_length=100) 
    bottom_text = models.CharField(max_length=100)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Meme by {self.created_by.username} using {self.template.name}"

# Rating Model
class Rating(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='ratings')  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating score (1 to 5)
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('meme', 'user')  # Ensure each user can only rate a meme once

    def __str__(self):
        return f"Rating {self.score} for meme by {self.user.username}"