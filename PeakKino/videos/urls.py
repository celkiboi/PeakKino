from django.urls import path
from .views import watch_video, upload_clip, video_details, all_videos, content_18_plus

app_name="videos"
urlpatterns = [
    path('<int:video_id>/', video_details, name='video_details'),
    path('<int:video_id>/watch/', watch_video, name="watch_video"),
    path('allvideos/', all_videos, name="all_videos"),
    path('18plus/', content_18_plus, name="18_plus"),
    path('upload/clip/', upload_clip, name='upload_clip'),
]