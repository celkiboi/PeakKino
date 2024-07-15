from django.urls import path
from .views import watch_video, upload_clip, video_details, all_videos, content_18_plus, delete_clip, upload_movie, delete_movie, all_movies, all_clips, create_show, search, update_timestamp, upload_subtitle, delete_subtitle, all_shows, show_details, create_season, upload_episode, delete_episode, delete_season, delete_show

app_name="videos"
urlpatterns = [
    path('<int:video_id>/', video_details, name='video_details'),
    path('<int:video_id>/watch/', watch_video, name="watch_video"),
    path('allvideos/', all_videos, name="all_videos"),
    path('allmovies/', all_movies, name="all_movies"),
    path('allclips/', all_clips, name="all_clips"),
    path('18plus/', content_18_plus, name="18_plus"),
    path('upload/clip/', upload_clip, name='upload_clip'),
    path('delete/clip/<int:clip_id>/', delete_clip, name="delete_clip"),
    path('upload/movie/', upload_movie, name='upload_movie'),
    path('delete/movie/<int:movie_id>/', delete_movie, name="delete_movie"),
    path('upload/show/', create_show, name="create_show"),
    path('search/', search, name="search"),
    path('<int:video_id>/updatetimestamp/', update_timestamp, name="update_timestamp"),
    path('upload/subtitle/<int:video_id>/', upload_subtitle, name="upload_subtitle"),
    path('delete/subtitle/<int:subtitle_id>/', delete_subtitle, name="delete_subtitle"),
    path('allshows/', all_shows, name="all_shows"),
    path('shows/<int:show_id>/', show_details, name="show_details"),
    path('upload/season/<int:show_id>/', create_season, name="create_season"),
    path('upload/episode/<int:season_id>/', upload_episode, name="upload_episode"),
    path('delete/episode/<int:episode_id>/', delete_episode, name="delete_episode"),
    path('delete/season/<int:season_id>/', delete_season, name="delete_season"),
    path('delete/show/<int:show_id>/', delete_show, name="delete_show"),
]