from django.shortcuts import render
from videos.models import Video, UserVideoTimestamp
from django.conf import settings
from django.urls import reverse

def home_view(request):
    timestamps = UserVideoTimestamp.objects.filter(user=request.user).order_by('-last_watched')
    videos = []
    for timestamp in timestamps:
        video = timestamp.video
        if request.user.can_view_content(video.get_resource()):
            attached_obj = video.get_attached_obj()
            thumbnail_path = settings.MEDIA_URL + video.get_thumbnail_path()
            details_page_url = reverse('videos:video_details', kwargs = {'video_id': video.pk})
            videos.append((video, thumbnail_path, attached_obj, details_page_url))
    context = {
        'videos': videos,
        'empty': len(videos) > 0,
    }
    return render(request, 'home.html', context)