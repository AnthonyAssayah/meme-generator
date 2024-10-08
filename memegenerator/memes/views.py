from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Meme
from .serializers import MemeSerializer


class MemeViewSet(viewsets.ModelViewSet):
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