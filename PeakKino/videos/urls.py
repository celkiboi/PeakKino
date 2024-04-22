from django.urls import path
from .views import watch_video, upload_clip, video_details, all_videos

app_name="videos"
urlpatterns = [
    path('<int:video_id>/', video_details, name='video_details'),
    path('<int:video_id>/watch/', watch_video, name="watch_video"),
    path('allvideos/', all_videos, name="all_videos"),
    path('upload/clip/', upload_clip, name='upload_clip'),
]