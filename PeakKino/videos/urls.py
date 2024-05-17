from django.urls import path
from .views import watch_video, upload_clip, video_details, all_videos, content_18_plus, delete_clip_page, delete_clip, upload_movie, delete_movie, delete_movie_page, all_movies, all_clips, create_show

app_name="videos"
urlpatterns = [
    path('<int:video_id>/', video_details, name='video_details'),
    path('<int:video_id>/watch/', watch_video, name="watch_video"),
    path('allvideos/', all_videos, name="all_videos"),
    path('allmovies/', all_movies, name="all_movies"),
    path('allclips/', all_clips, name="all_clips"),
    path('18plus/', content_18_plus, name="18_plus"),
    path('upload/clip/', upload_clip, name='upload_clip'),
    path('delete/clip/', delete_clip_page, name="delete_clip_page"),
    path('delete/clip/<int:clip_id>/', delete_clip, name="delete_clip"),
    path('upload/movie/', upload_movie, name='upload_movie'),
    path('delete/movie/', delete_movie_page, name="delete_movie_page"),
    path('delete/movie/<int:movie_id>/', delete_movie, name="delete_movie"),
    path('upload/show/', create_show, name="create_show"),
]