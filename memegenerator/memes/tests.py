from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Meme, MemeTemplate
from django.contrib.auth.models import User

class MemeAPIViewsTest(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

          # Create meme templates
        self.template1 = MemeTemplate.objects.create(
            name="Template 1",
            image_url="https://example.com/template1.jpg",
            default_top_text="Top Text 1",
            default_bottom_text="Bottom Text 1"
        )
        self.template2 = MemeTemplate.objects.create(
            name="Template 2",
            image_url="https://example.com/template2.jpg",
            default_top_text="Top Text 2",
            default_bottom_text="Bottom Text 2"
        )

        # Create memes
        self.meme1 = Meme.objects.create(
            template=self.template1,
            top_text="Custom Top Text 1",
            bottom_text="Custom Bottom Text 1",
            created_by=self.user1
        )
        self.meme2 = Meme.objects.create(
            template=self.template2,
            top_text="Custom Top Text 2",
            bottom_text="Custom Bottom Text 2",
            created_by=self.user2
        )