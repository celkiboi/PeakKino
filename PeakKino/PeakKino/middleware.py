from django.http import HttpResponseForbidden
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from videos.models import Resource
from django.shortcuts import get_object_or_404
import os
from videos.models import Video

class CheckAuthentificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith(settings.MEDIA_URL):
            return HttpResponseForbidden("You are not authorized to access this resource.")
        
        if request.path.startswith(settings.MEDIA_URL):
            id = int(request.path.split('/')[2])
            resource = get_object_or_404(Resource, pk=id)
            if not request.user.can_view_content(resource):
                return HttpResponseForbidden(f"Your age does not permit you to view {resource.age_rating}+ content")
        
        response = self.get_response(request)
        return response

'''
Videos are huge (in size), and the way Django serves them doesn't allow for rewinding
With this, we can freely rewind the video
This Middleware ensures we can actually stream the video, not just send it
'''
class RangesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code != 200 or not hasattr(response, "file_to_stream"):
            return response
        http_range = request.META.get("HTTP_RANGE")
        if not (
            http_range
            and http_range.startswith("bytes=")
            and http_range.count("-") == 1
        ):
            return response
        if_range = request.META.get("HTTP_IF_RANGE")
        if (
            if_range
            and if_range != response.get("Last-Modified")
            and if_range != response.get("ETag")
        ):
            return response
        f = response.file_to_stream
        statobj = os.fstat(f.fileno())
        start, end = http_range.split("=")[1].split("-")
        if not start:  
            start = max(0, statobj.st_size - int(end))
            end = ""
        start, end = int(start or 0), int(end or statobj.st_size - 1)
        assert 0 <= start < statobj.st_size, (start, statobj.st_size)
        end = min(end, statobj.st_size - 1)
        f.seek(start)
        old_read = f.read
        f.read = lambda n: old_read(min(n, end + 1 - f.tell()))
        response.status_code = 206
        response["Content-Length"] = end + 1 - start
        response["Content-Range"] = "bytes %d-%d/%d" % (start, end, statobj.st_size)
        return response