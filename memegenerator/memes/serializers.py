from rest_framework import serializers
from .models import MemeTemplate, Meme, Rating
from django.contrib.auth.models import User

class MemeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemeTemplate
        fields = ['id', 'name', 'image_url', 'default_top_text', 'default_bottom_text']

class MemeSerializer(serializers.ModelSerializer):
    
    # Set default values for top_text and bottom_text
    top_text = serializers.CharField(default="Default Top Text", required=False)
    bottom_text = serializers.CharField(default="Default Bottom Text", required=False)
    
    class Meta:
        model = Meme
        fields = ['id', 'template', 'top_text', 'bottom_text', 'created_by', 'created_at']

    def create(self, validated_data):
       
        template = validated_data.get('template')
        created_by = validated_data.get('created_by')

        # Use the authenticated user if created_by is not provided
        if not created_by:
            created_by = self.context['request'].user

        # Use template's default values if provided
        top_text = validated_data.get('top_text', template.default_top_text if template else 'Default Top Text')
        bottom_text = validated_data.get('bottom_text', template.default_bottom_text if template else 'Default Bottom Text')

       
        meme = Meme.objects.create(
            template=template,
            top_text=top_text,
            bottom_text=bottom_text,
            created_by=created_by
        )
        return meme


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'meme', 'user', 'score', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
