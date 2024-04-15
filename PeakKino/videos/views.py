from django.shortcuts import render, get_object_or_404
from .models import Video
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    context = {
        'video' : video,
        'path' : settings.MEDIA_URL + video.path
    }
    return render(request, 'watch_video.html', context)