from django.urls import path
from .views import watch_video, upload_clip

app_name="videos"
urlpatterns = [
    path('<int:video_id>/watch', watch_video, name="watch_video"),
    path('upload/clip', upload_clip, name='upload_clip'),
]