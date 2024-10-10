from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Meme, MemeTemplate, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

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

        
    # Test for GET /api/memes/<id>/ (Retrieve a specific meme)
    def test_retrieve_meme(self):
        url = reverse('meme-detail', args=[self.meme1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.meme1.id)
        self.assertEqual(response.data['top_text'], self.meme1.top_text)
    
    # Test retrieve meme with invalid ID    
    def test_retrieve_non_existent_meme(self):
        url = reverse('meme-detail', args=[9999])  # Non-existent meme ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  
        self.assertIn('detail', response.data)
    
    # Test retrieve meme with valid data structure
    def test_retrieve_meme_data_structure(self):
        url = reverse('meme-detail', args=[self.meme1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for the presence of all expected fields in the response
        expected_fields = {'id', 'template', 'top_text', 'bottom_text', 'created_by', 'created_at'}
        self.assertTrue(expected_fields.issubset(response.data.keys()))

        # checks for field types
        self.assertIsInstance(response.data['id'], int)
        self.assertIsInstance(response.data['template'], int)
        self.assertIsInstance(response.data['top_text'], str)
        self.assertIsInstance(response.data['bottom_text'], str)
        self.assertIsInstance(response.data['created_by'], int)
        self.assertIsInstance(response.data['created_at'], str)


    # Test retrieve meme for deleted meme
    def test_retrieve_deleted_meme(self):
        self.meme1.delete()
        url = reverse('meme-detail', args=[self.meme1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should return 404 after deletion
        self.assertIn('detail', response.data)  

    # Test retrive meme with large data payload
    def test_retrieve_meme_large_payload(self):
        large_text = 'A' * 100
        meme = Meme.objects.create(
            template=self.template1,
            top_text=large_text,
            bottom_text=large_text,
            created_by=self.user1
        )
        url = reverse('meme-detail', args=[meme.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['top_text'], large_text)
        self.assertEqual(response.data['bottom_text'], large_text)


    # Test for POST /api/memes/<id>/rate/ (Rate a meme)
    def test_rate_meme(self):
        url = reverse('meme-rate-meme', args=[self.meme1.id]) 
        data = {'rating': 4}
        
        token = Token.objects.get(user__username='user1')
        client = APIClient()

        # Set the authorization header with the token
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1) 
        
    
    # Test rating with invalid range value
    def test_rate_meme_invalid_rating(self):
        url = reverse('meme-rate-meme', args=[self.meme1.id])
        invalid_data = {'rating': 6}  # Rating outside the valid range (1-5)
        
        token = Token.objects.get(user__username='user1')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)  
        self.assertEqual(Rating.objects.count(), 0)  # Rating should not be created
    
    # Test user rating the same meme twice    
    def test_rate_meme_update_existing_rating(self):
        url = reverse('meme-rate-meme', args=[self.meme1.id])
        initial_data = {'rating': 3}
        
        # First request with a rating of 3
        token = Token.objects.get(user__username='user1')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = client.post(url, initial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().score, 3)  # Rating should be 3
        
        # Second request with a new rating of 4
        updated_data = {'rating': 4}
        response = client.post(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1)  
        self.assertEqual(Rating.objects.first().score, 4)  # Rating should now be 4


    # Test for GET /api/memes/random/ (Get a random meme)
    def test_random_meme(self):
        url = reverse('meme-get-random-meme')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)  # Should return a meme with an 'id' field
        
    # Test for GET /api/memes/random/ when no memes exist
    def test_random_meme_no_memes(self):
        # Clear all memes
        Meme.objects.all().delete()
        
        url = reverse('meme-get-random-meme')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'No memes found')
    
    # Test for GET /api/memes/random/ to ensure randomness
    def test_random_meme_randomness(self):
        Meme.objects.create( template=self.template1,
                            top_text="Custom Top Text 1",
                            bottom_text="Custom Bottom Text 1",
                            created_by=self.user1)
        Meme.objects.create( template=self.template2,
                            top_text="Custom Top Text 2",
                            bottom_text="Custom Bottom Text 2",
                            created_by=self.user2)
        Meme.objects.create( template=self.template3,
                            top_text="Custom Top Text 3",
                            bottom_text="Custom Bottom Text 3",
                            created_by=self.user2)

        url = reverse('meme-get-random-meme')
        
        response1 = self.client.get(url)
        meme_id_1 = response1.data['id']
        response2 = self.client.get(url)
        meme_id_2 = response2.data['id']
        
        # Check that the two responses are different (high probability)
        self.assertNotEqual(meme_id_1, meme_id_2)

