from django.shortcuts import render, get_object_or_404
from .models import Video, Resource
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

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