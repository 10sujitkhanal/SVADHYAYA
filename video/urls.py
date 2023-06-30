from django.urls import path
from .views import VideoPageView, VideoDetailView, VideoListView

urlpatterns = [
    path('', VideoPageView.as_view(), name='video'),
    path('<str:pk>/', VideoDetailView.as_view(), name='video_detail_view'),
    path('v/list/', VideoListView.as_view(), name='video_list'),  
]