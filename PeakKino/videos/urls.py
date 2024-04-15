from django.urls import path
from .views import watch_video

app_name="videos"
urlpatterns = [
    path('<int:video_id>/watch', watch_video, name="watch_video")
]