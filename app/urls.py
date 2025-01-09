from django.urls import path
from .views import CategoryListView, VideoListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/videos/', VideoListView.as_view(), name='video-list'),
]
