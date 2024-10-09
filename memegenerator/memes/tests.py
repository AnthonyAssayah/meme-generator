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
        self.template3 = MemeTemplate.objects.create(
            name="Template 3",
            image_url="https://example.com/template3.jpg",
            default_top_text="Top Text 3",
            default_bottom_text="Bottom Text 3"
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
        
    # Test for GET /api/templates/ (List all meme templates)
    def test_list_templates(self):
        url = reverse('template-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  
        self.assertEqual(response.data[0]['name'], self.template1.name)
        self.assertEqual(response.data[1]['image_url'], self.template2.image_url)
        self.assertIn('Text', response.data[2]['default_top_text'])
    
    # Edge case: No templates available
    def test_list_templates_empty(self):
        MemeTemplate.objects.all().delete()  # Delete all templates
        url = reverse('template-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return an empty list


    # Negative test: Incorrect URL (404 error)
    def test_invalid_url(self):
        url = '/api/invalid_templates/'  # Invalid URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should return 404

    # Test: Ensure image URL contains "example.com"
    def test_image_url_contains_example(self):
        url = reverse('template-list')
        response = self.client.get(url)
        for template in response.data:
            self.assertIn('example.com', template['image_url']) 
            
    
     # Test for GET /api/memes/ (List all memes with pagination)
    def test_list_memes(self):
        url = reverse('meme-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        self.assertEqual(len(response.data), 4)  
        self.assertEqual(response.data['results'][0]['top_text'], self.meme1.top_text)

    