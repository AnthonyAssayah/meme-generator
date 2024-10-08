from django.db import models
from django.contrib.auth.models import User

# MemeTemplate Model
class MemeTemplate(models.Model):
    name = models.CharField(max_length=100)  
    image_url = models.URLField()  
    default_top_text = models.CharField(max_length=100, blank=True) 
    default_bottom_text = models.CharField(max_length=100, blank=True)  

    def __str__(self):
        return self.name