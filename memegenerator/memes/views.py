from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django.db.models import Avg

from .models import Meme, MemeTemplate, Rating
from .serializers import MemeSerializer, MemeTemplateSerializer, RatingSerializer



class MemeTemplateViewSet(viewsets.ModelViewSet):
    queryset = MemeTemplate.objects.all()
    serializer_class = MemeTemplateSerializer

    # GET /api/templates/ - List all meme templates
    def list(self, request):
        queryset = self.get_queryset()
        serializer = MemeTemplateSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    # POST /api/templates/ - Create a new meme template
    def create(self, request):
        serializer = MemeTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class MemeViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    pagination_class = PageNumberPagination  # This will handle pagination

    # GET /api/memes/ - List all memes (with pagination)
    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MemeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MemeSerializer(queryset, many=True)
        return Response(serializer.data)


    # POST /api/memes/ - Create a new meme
    def create(self, request):
        serializer = MemeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
    # GET /api/memes/<id>/ - Retrieve a specific meme
    def retrieve(self, request, pk=None):
        meme = self.get_object()
        serializer = MemeSerializer(meme)
        return Response(serializer.data)
    
    
    # POST /api/memes/<id>/rate/: Rate a meme
    @action(detail=True, methods=['post'], url_path='rate')
    def rate_meme(self, request, pk=None):
        meme = self.get_object()
        rating = request.data.get('rating')

        if not (1 <= rating <= 5):
            return Response({"error": "Rating must be between 1 and 5"}, status=400)

        user_rating = meme.ratings.filter(user=request.user)
        if user_rating.exists():
            user_rating.update(score=rating)
        else:
            meme.ratings.create(user=request.user, score=rating)
        
        return Response({'status': 'rated'})
    
    
    # GET /api/memes/random/ - Get a random meme
    @action(detail=False, methods=['get'], url_path='random')
    def get_random_meme(self, request):
        random_meme = Meme.objects.order_by('?').first()  # Random meme
        if random_meme:
            serializer = MemeSerializer(random_meme)
            return Response(serializer.data)
        return Response({"error": "No memes found"}, status=status.HTTP_404_NOT_FOUND)


    # GET /api/memes/top/ - Get top 10 rated memes
    @action(detail=False, methods=['get'], url_path='top')
    def get_top_rated_memes(self, request):
        # Calculate the average rating for each meme
        top_memes = Meme.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')[:10]
        serializer = MemeSerializer(top_memes, many=True)
        return Response(serializer.data)
    
    
class RatingViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    # GET /api/ratings/ - List all ratings
    def list(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)