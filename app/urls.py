from django.urls import path
from .views import CategoryListView, VideoListView
from .views import signup_view, dashboard, category_videos, SingleLoginView, logout_view

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/videos/', VideoListView.as_view(), name='video-list'),
    path('signup/', signup_view, name='signup'),
    path('', SingleLoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('category/<int:category_id>/', category_videos, name='category_videos'),
    path('logout/', logout_view, name='logout'),
]
