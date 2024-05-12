from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, Resource, Clip, Movie
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, JsonResponse
from .forms import ClipUploadForm, MovieUploadForm
from .decorators import staff_required
from django.urls import reverse
from .utils import delete_folder

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    resource = video.get_resource()

    if not request.user.can_view_content(resource):
        return HttpResponseForbidden(f"Your age does not permit you to view {resource.age_rating}+ content")

    context = {
        'title' : video.get_attached_obj().title,
        'path' : settings.MEDIA_URL + video.get_path()
    }
    return render(request, 'watch_video.html', context)

@login_required
@staff_required
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
def video_details(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    resource = video.get_resource()

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
        'video_path': video_path
    }

    return render(request, 'video_details.html', context)

@login_required
def all_videos(request):
    videos = Video.objects.all()

    filtered_videos = []
    for video in videos:
        if request.user.can_view_content(video.get_resource()):
            attached_obj = video.get_attached_obj()
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
            filtered_videos.append((video, thumbnail_path, attached_obj, details_page_url))

    context = {
        'videos': filtered_videos,
    }
    
    return render(request, 'all_videos.html', context)

@login_required
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
    
    context = {
        'videos': filtered_videos,
    }
    
    return render(request, '18_plus.html', context)

@staff_required
@login_required
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
@require_POST
def delete_clip(request, clip_id):
    clip = get_object_or_404(Clip, pk=clip_id)
    video = clip.video
    resource = video.get_resource()
    path = f"{settings.MEDIA_ROOT}/{resource.pk}"

    delete_folder(path)
    clip.delete()
    video.delete()
    resource.delete()

    return JsonResponse({'success': True, 'message': 'Clip deleted succesfully'})

@login_required
@staff_required
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
@require_POST
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    video = movie.video
    resource = video.get_resource()
    path = f"{settings.MEDIA_ROOT}/{resource.pk}"

    delete_folder(path)
    movie.delete()
    video.delete()
    resource.delete()

    return JsonResponse({'success': True, 'message': 'Movie deleted succesfully'})

@login_required
def all_movies(request):
    movies = Movie.objects.all()

    filtered_movies = []
    for movie in movies:
        if request.user.can_view_content(movie.resource):
            video = movie.video
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
            filtered_movies.append((video, thumbnail_path, movie, details_page_url))
    context = {
        'videos': filtered_movies,
    }
    
    return render(request, 'all_videos.html', context)

@login_required
def all_clips(request):
    clips = Clip.objects.all()

    filtered_clips = []
    for clip in clips:
        if request.user.can_view_content(clip.resource):
            video = clip.video
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs= {'video_id': video.pk})
            filtered_clips.append((video, thumbnail_path, clip, details_page_url))
    context = {
        'videos': filtered_clips
    }

    return render(request, 'all_videos.html', context)