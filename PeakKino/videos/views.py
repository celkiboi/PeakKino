from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, Resource
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ClipUploadForm
from .decorators import staff_required
from django.urls import reverse

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
    return render(request, 'upload_clip.html', {'form': form})

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
    