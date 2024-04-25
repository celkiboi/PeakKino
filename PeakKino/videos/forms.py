from django import forms
from django.conf import settings
from .models import Clip, Resource, Video, Movie
from django.core.exceptions import ValidationError
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import cv2
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models

class UploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['resource_age_rating', 'upload']
    
    
    def handle_uploaded_file(self, uploaded_file, video):
        path = f'{settings.MEDIA_ROOT}/{video.get_path()}'
        print(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

    def validate_file_extension(value):
        valid_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        extension = os.path.splitext(value.name)[1]
        if extension not in valid_extensions:
            raise ValidationError('Unsupported file extension')

    resource_age_rating = forms.ChoiceField(choices=Resource.AGE_RATING_CHOICES)
    upload = forms.FileField(
        validators=[validate_file_extension],
        widget=forms.FileInput(attrs={'accept':'.mp4,.avi,.mov,.mkv'})
    )

    def generate_thumbnail(self, uploaded_file, video_obj: Video):
        video = cv2.VideoCapture(uploaded_file.temporary_file_path())
        success, frame = video.read()
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video.release()

        if not success:
            raise ValidationError('Failed to read video frame')

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        thumbnail_image = Image.fromarray(frame_rgb)
        thumbnail_image.thumbnail((width, height))

        thumbnail_buffer = BytesIO()
        thumbnail_image.save(thumbnail_buffer, format='WEBP')
        thumbnail_buffer.seek(0)

        thumbnail_content = ContentFile(thumbnail_buffer.getvalue())
        thumbnail_name = f'{video_obj.uuid}.webp'
        thumbnail_path = settings.MEDIA_ROOT + '/' + video_obj.get_thumbnail_path()

        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        with open(thumbnail_path, 'wb+') as destination:
            destination.write(thumbnail_content.read())

        return thumbnail_name

class MovieUploadForm(UploadForm):
    class Meta(UploadForm.Meta):
        model = Movie
        fields = UploadForm.Meta.fields + ['lead_actor', 'director', 'title']

    def save(self, commit=True):
        movie = super().save(commit=False)

        age_rating = self.cleaned_data['resource_age_rating']
        resource = Resource.objects.create(age_rating=age_rating)

        uploaded_file = self.cleaned_data['upload']
        name, extension = os.path.splitext(str(uploaded_file))

        video = Video.objects.create(type='movie', extension=extension)

        movie.resource = resource
        movie.video = video

        if commit:
            movie.save()
            video.save()
        
        self.generate_thumbnail(uploaded_file, video)

        self.handle_uploaded_file(uploaded_file, video)
        return movie

class ClipUploadForm(UploadForm):
    class Meta(UploadForm.Meta):
        model = Clip
        fields = UploadForm.Meta.fields + ['title']  

    def save(self, commit=True):
        clip = super().save(commit=False)

        age_rating = self.cleaned_data['resource_age_rating']
        resource = Resource.objects.create(age_rating=age_rating)

        uploaded_file = self.cleaned_data['upload']
        name, extension = os.path.splitext(str(uploaded_file))

        video = Video.objects.create(type='clip', extension=extension)

        clip.resource = resource
        clip.video = video

        if commit:
            clip.save()
            video.save()
        
        self.generate_thumbnail(uploaded_file, video)

        self.handle_uploaded_file(uploaded_file, video)
        return clip

