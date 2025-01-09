from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Category, Video
from .serializers import CategorySerializer, VideoSerializer

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class VideoListView(APIView):
    def post(self, request, category_id):
        category = Category.objects.get(id=category_id)
        password = request.data.get('password')

        if category.password != password:
            raise AuthenticationFailed('Incorrect password')

        videos = Video.objects.filter(category=category)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
