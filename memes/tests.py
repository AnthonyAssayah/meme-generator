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


    # Edge case: no meme avaliables 
    def test_list_memes_empty(self):
        Meme.objects.all().delete()  # Delete all memes 
        url = reverse('meme-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)
        
    # Test for checking pagaination
    def test_list_memes_pagination(self):
        url = reverse('meme-list')
        # Assuming pagination is set to 2 per page
        for i in range(5):  # Create 5 memes
            Meme.objects.create(
                template=self.template1, top_text=f"Top {i}", bottom_text=f"Bottom {i}", created_by=self.user1
            )
        response = self.client.get(url, {'page': 1})  # Request page 1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)  
        self.assertIn('previous', response.data)  
        
      
    # Test for invalid pagination  
    def test_list_memes_invalid_pagination(self):
        url = reverse('meme-list')
        response = self.client.get(url, {'page': 999})  # Request a non-existent page
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data) 
    
    # Test meme content validation
    def test_list_memes_structure(self):
        url = reverse('meme-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for meme in response.data['results']:
            self.assertIn('id', meme)
            self.assertIn('template', meme)
            self.assertIn('top_text', meme)
            self.assertIn('bottom_text', meme)
            self.assertIn('created_by', meme)
            self.assertIn('created_at', meme)


    # Test for POST /api/memes/ (Create a new meme) - POST /api/templates/ (Create a new memeTemplate)
    def test_create_meme_and_memeTemplate(self):
        url = reverse('meme-list')
        data = {
            'template': self.template1.id,
            'top_text': 'New Top Text',
            'bottom_text': 'New Bottom Text',
            'created_by': self.user1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meme.objects.count(), 3)  # Should now have 3 memes
        
        url2 = reverse('template-list')
        data2 = {
            'name': "Template 4",
            'image_url': "https://example.com/template4.jpg",
            'default_top_text': "Top Text 4",
            'default_bottom_text': "Bottom Text 4"
        }
        response2 = self.client.post(url2, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
    
    # Test creating meme without required fields 
    def test_create_meme_missing_required_fields(self):
        url = reverse('meme-list')
        data = {
            'template': self.template1.id,
            'bottom_text': 'New Bottom Text',
            'top_text': 'New Top Text',
            # Missing required 'created_by'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    # Test creating template without required fields  
    def test_create_template_missing_required_fields(self):
        url = reverse('template-list')
        data = {
            'url': 'http://example.com/template.jpg',  # Missing 'name'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)  # Error for missing field
        
        
    # Test for invalid template ID and user ID
    def test_create_meme_invalid_fields(self):
        url = reverse('meme-list')
        data = {
            'template': 9999,  # Non-existent template ID
            'top_text': 'Invalid Template',
            'bottom_text': 'Invalid Template',
            'created_by': self.user1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('template', response.data)  # Error message for invalid template
        
        data1 = {
            'template': self.template1.id,
            'top_text': 'Invalid User',
            'bottom_text': 'Invalid User',
            'created_by': 9999  # Non-existent user ID
        }
        response1 = self.client.post(url, data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('created_by', response1.data)  # Error message for invalid user ID
    
    
    # Test for invalid json format
    def test_create_meme_invalid_json_format(self):
        url = reverse('meme-list')
        invalid_data = 'Invalid JSON data'
        response = self.client.post(url, invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)  # Generic error for bad request


    # Test creating template with existing url
    def test_create_template_duplicate_url(self):
        url = reverse('template-list')
        data = {
            'name': 'Duplicate URL Template',
            'image_url': self.template1.image_url,  # Use the same URL as an existing template
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  


    