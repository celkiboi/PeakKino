from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, Resource, Clip, Movie, UserVideoTimestamp, Subtitle, Show
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from .forms import ClipUploadForm, MovieUploadForm, ShowCreateForm, SubtitleUploadForm
from accounts.decorators import staff_required, approval_required
from django.urls import reverse
from .utils import delete_folder
from .config import VIDEO_WATCH_UPDATE_INTERVAL
from datetime import datetime
import os

@login_required
@approval_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    resource = video.get_resource()
    subtitles = Subtitle.objects.filter(video=video)

    user_video_timestamp = UserVideoTimestamp.objects.filter(video=video, user=request.user).first()
    timestamp = 0
    if user_video_timestamp is not None:
        timestamp = user_video_timestamp.timestamp

    if not request.user.can_view_content(resource):
        return HttpResponseForbidden(f"Your age does not permit you to view {resource.age_rating}+ content")

    subs = []
    for subtitle in subtitles:
        subs.append((subtitle.language, '/media/' + subtitle.get_file_path()))

    context = {
        'title' : video.get_attached_obj().title,
        'path' : settings.MEDIA_URL + video.get_path(),
        'updateInterval': VIDEO_WATCH_UPDATE_INTERVAL,
        'id': video.id,
        'timestamp': timestamp,
        'subtitles': subs,
    }
    return render(request, 'watch_video.html', context)

@login_required
@staff_required
@approval_required
def upload_clip(request):
    if request.method == 'POST':
        form = ClipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            clip = form.save(commit=True)
            uploaded_file = request.FILES['upload']
            return redirect('/')  
    else:
        form = ClipUploadForm()
    return render(request, 'upload.html', {'form': form, 'type': 'Clip'})

@login_required
@approval_required
def video_details(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    resource = video.get_resource()
    subtitles = Subtitle.objects.filter(video=video)

    if not request.user.can_view_content(resource):
        return HttpResponseForbidden(f"Your age does not permit you to view {resource.age_rating}+ content")
    
    # get a movie/episode/clip object, depending on the video type
    attached_obj = video.get_attached_obj()
    thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
    video_path = reverse('videos:watch_video', kwargs={'video_id': video_id})


    context = {
        'video': video,
        'resource': resource,
        'attached_obj': attached_obj,
        'thumbnail_path': thumbnail_path,
        'video_path': video_path,
        'subtitles': subtitles,
    }

    return render(request, 'video_details.html', context)

@login_required
@approval_required
def all_videos(request):
    videos = Video.objects.all()

    filtered_videos = []
    for video in videos:
        if request.user.can_view_content(video.get_resource()):
            attached_obj = video.get_attached_obj()
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
            filtered_videos.append((video, thumbnail_path, attached_obj, details_page_url))

    query = request.GET.get('query', '')
    if query != '':
        queried_videos = []
        
        for video_tuple in filtered_videos:
            video = video_tuple[0]
            if query.lower() in video.get_attached_obj().title.lower():
                queried_videos.append(video_tuple)
    
        filtered_videos = queried_videos
    else:
        query = 'Search for videos...'

    context = {
        'videos': filtered_videos,
        'query': query,
        'type': 'all'
    }
    
    return render(request, 'all_videos.html', context)

@login_required
@approval_required
def content_18_plus(request):
    if request.user.age < 18:
        return HttpResponseForbidden(f"Your age does not permit you to view 18+ content")
    
    filtered_videos = []
    videos = Video.objects.all()
    for video in videos:
        if video.get_resource().age_rating == '18':
            attached_obj = video.get_attached_obj()
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
            filtered_videos.append((video, thumbnail_path, attached_obj, details_page_url))
    
    query = request.GET.get('query', '')
    if query != '':
        queried_videos = []
        
        for video_tuple in filtered_videos:
            video = video_tuple[0]
            if query.lower() in video.get_attached_obj().title.lower():
                queried_videos.append(video_tuple)
    
        filtered_videos = queried_videos
    else:
        query = 'Search for videos...'

    context = {
        'videos': filtered_videos,
        'query': query,
        'type': 'all',
    }
    
    return render(request, '18_plus.html', context)

@staff_required
@login_required
@approval_required
def delete_clip_page(request):
    clips = Clip.objects.all()

    render_collection = []
    for clip in clips:
        video = clip.video
        thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
        details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
        id = clip.pk
        render_collection.append((video, thumbnail_path, clip, details_page_url, id))
    
    context = {
            'render_collection': render_collection,
            'type': 'clip'
        }

    return render(request, 'delete.html', context)

@staff_required
@login_required
@approval_required
@require_POST
def delete_clip(request, clip_id):
    clip = get_object_or_404(Clip, pk=clip_id)
    video = clip.video
    resource = video.get_resource()
    path = f"{settings.MEDIA_ROOT}/{resource.pk}"
    user_video_timestamps = UserVideoTimestamp.objects.filter(video=video)
    subtitles = Subtitle.objects.filter(video=video)
    for subtitle in subtitles:
        delete_subtitle(request, subtitle.id)

    for timestamp in user_video_timestamps:
        timestamp.delete()
    delete_folder(path)
    clip.delete()
    video.delete()
    resource.delete()

    return JsonResponse({'success': True, 'message': 'Clip deleted succesfully'})

@login_required
@staff_required
@approval_required
def upload_movie(request):
    if request.method == 'POST':
        form = MovieUploadForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=True)
            uploaded_file = request.FILES['upload']
            return redirect('/')  
    else:
        form = MovieUploadForm()
    return render(request, 'upload.html', {'form': form, 'type': 'Movie'})

@staff_required
@login_required
@approval_required
def delete_movie_page(request):
    movies = Movie.objects.all()

    render_collection = []
    for movie in movies:
        video = movie.video
        thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
        details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
        id = movie.pk
        render_collection.append((video, thumbnail_path, movie, details_page_url, id))
    
    context = {
            'render_collection': render_collection,
            'type': 'movie'
        }

    return render(request, 'delete.html', context)

@staff_required
@login_required
@approval_required
@require_POST
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    video = movie.video
    resource = video.get_resource()
    path = f"{settings.MEDIA_ROOT}/{resource.pk}"
    user_video_timestamps = UserVideoTimestamp.objects.filter(video=video)
    subtitles = Subtitle.objects.filter(video=video)
    for subtitle in subtitles:
        delete_subtitle(request, subtitle.id)

    for timestamp in user_video_timestamps:
        timestamp.delete()
    delete_folder(path)
    movie.delete()
    video.delete()
    resource.delete()

    return JsonResponse({'success': True, 'message': 'Movie deleted succesfully'})

@login_required
@approval_required
def all_movies(request):
    movies = Movie.objects.all()

    filtered_movies = []
    for movie in movies:
        if request.user.can_view_content(movie.resource):
            video = movie.video
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
            filtered_movies.append((video, thumbnail_path, movie, details_page_url))
   
    query = request.GET.get('query', '')
    if query != '':
        queried_movies = []
        
        for movie_tuple in filtered_movies:
            movie = movie_tuple[2]
            if query.lower() in movie.title.lower():
                queried_movies.append(movie_tuple)
    
        filtered_movies = queried_movies
    else:
        query = 'Search for movies...'

    context = {
        'videos': filtered_movies,
        'query': query,
        'type': 'movies',
    }
    
    return render(request, 'all_videos.html', context)

@login_required
@approval_required
def all_clips(request):
    clips = Clip.objects.all()

    filtered_clips = []
    for clip in clips:
        if request.user.can_view_content(clip.resource):
            video = clip.video
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs= {'video_id': video.pk})
            filtered_clips.append((video, thumbnail_path, clip, details_page_url))
    
    query = request.GET.get('query', '')
    if query != '':
        queried_clips = []
        
        for clip_tuple in filtered_clips:
            clip = clip_tuple[2]
            if query.lower() in clip.title.lower():
                queried_clips.append(clip_tuple)
    
        filtered_clips = queried_clips
    else:
        query = 'Search for clips...'

    context = {
        'videos': filtered_clips,
        'query': query,
        'type': 'clips',
    }
    
    return render(request, 'all_videos.html', context)

@login_required
@staff_required
@approval_required
def create_show(request):
    if request.method == 'POST':
        form = ShowCreateForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save(commit=True)
            return redirect('/')
    else:
        form = ShowCreateForm()
    return render(request, 'upload_show.html', {'form': form, 'type': 'Show'})

@login_required
@approval_required
def search(request):
    query = request.GET.get('query', '')
    type = request.GET.get('type', '')
    if type not in ['all', 'movies', 'clips', 'shows', '18plus']:
        return HttpResponseBadRequest()

    url = ''
    if type == 'all':
        url = reverse('videos:all_videos') + f'?query={query}'
    elif type == 'movies':
        url = reverse('videos:all_movies') + f'?query={query}'
    elif type == 'clips':
        url = reverse('videos:all_clips') + f'?query={query}'
    elif type == 'shows':
        url = reverse('videos:all_shows') + f'?query={query}'
    elif type == '18plus':
        url = reverse('videos:18_plus') + f'?query={query}'
    
    return redirect(url)

@login_required
@approval_required
@require_POST
def update_timestamp(request, video_id):
    video = Video.objects.filter(id=video_id).first()
    timestamp = int(float(request.POST.get('timestamp', 0)))
    user = request.user

    user_video_timestamp, created = UserVideoTimestamp.objects.get_or_create(
        user=user,
        video=video,
        defaults={'timestamp': timestamp}
    )

    if not created:
        user_video_timestamp.timestamp = timestamp
        user_video_timestamp.last_watched = datetime.now()
        user_video_timestamp.save()
    
    response_data = {
        'status': 'success',
        'timestamp': user_video_timestamp.timestamp,
    }

    return JsonResponse(response_data)

@login_required
@staff_required
def upload_subtitle(request, video_id):
    if request.method == 'POST':
        form = SubtitleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            subtitle = form.save(commit=True, video_id=video_id)
            return redirect('/')
    else:
        form = SubtitleUploadForm()
    return render(request, 'upload.html', {'form': form, 'type': 'Subtitle'})

@login_required
@staff_required
@require_POST
def delete_subtitle(request, subtitle_id):
    subtitle = get_object_or_404(Subtitle, id=subtitle_id)
    path = f"{settings.MEDIA_ROOT}/{subtitle.get_file_path()}"

    if os.path.exists(path):
        os.remove(path)

    subtitle.delete()
    return JsonResponse({'success': True, 'message': 'Subtitle deleted succesfully'})

@login_required
@staff_required
def all_shows(request):
    shows = Show.objects.all()
    user = request.user

    filtered_shows = []
    for show in shows:
        if user.can_view_content(show.resource):
            filtered_shows.append(show)
    
    query = request.GET.get('query', '')
    if query != '':
        queried_shows = []

        for show in filtered_shows:
            if query.lower() in show.name.lower():
                queried_shows.append(show)

        filtered_shows = queried_shows
    else:
        query = 'Search for shows...'

    context = {
        'shows': filtered_shows,
        'query': query,
        'type': 'shows'
    }

    return render(request, 'all_shows.html', context)