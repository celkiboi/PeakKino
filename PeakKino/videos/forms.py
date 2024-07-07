from django import forms
from django.conf import settings
from .models import Clip, Resource, Video, Movie, Show, Subtitle
from django.core.exceptions import ValidationError
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import cv2
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from .utils import srt_to_vtt

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

class ShowCreateForm(forms.ModelForm):
    image_upload = forms.ImageField(label='Upload Image', required=True)

    class Meta:
        model = Show
        fields = ['name', 'resource_age_rating', 'image_upload']

    resource_age_rating = forms.ChoiceField(choices=Resource.AGE_RATING_CHOICES)

    def convert_to_webp(self, image):
        img = Image.open(image)

        webp_image = BytesIO()
        img.save(webp_image, 'WEBP')

        webp_image.seek(0)
        webp_file = InMemoryUploadedFile(webp_image, None, image.name.split('.')[0] + '.webp', 'image/webp', webp_image.tell(), None)

        return webp_file

    def save(self, commit=True):
        show = super().save(commit=False)

        age_rating = self.cleaned_data['resource_age_rating']
        resource = Resource.objects.create(age_rating=age_rating)

        name = self.cleaned_data['name']

        show.resource = resource
        show.name = name

        if self.cleaned_data.get('image_upload'):
            image = self.cleaned_data['image_upload']
            webp_image = self.convert_to_webp(image)
            image_name = "image.webp"
            path = settings.MEDIA_ROOT + '/' + show.get_image_path()

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb+') as destination:
                destination.write(webp_image.read())

        if commit:
            show.save()
        
        return show

class SubtitleUploadForm(forms.ModelForm):
    subtitle_upload = forms.FileField(label='Upload Subtitle', required=True)

    class Meta:
        model = Subtitle
        fields = [ 'language', 'subtitle_upload']

        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'language': 'Subtitle Language',
        }
    
    def save(self, video_id, commit=True):
        subtitle = super().save(commit=False)
        subtitle.video = Video.objects.filter(id=video_id).first()

        if self.cleaned_data.get('subtitle_upload'):
            subtitle_file = self.cleaned_data['subtitle_upload']
            vtt_content = ""
            _, file_extension = os.path.splitext(subtitle_file.name)
            if file_extension == ".srt":
                try:
                    srt_content = subtitle_file.read().decode('utf-8')
                except UnicodeDecodeError:
                    subtitle_file.seek(0)
                    srt_content = subtitle_file.read().decode('iso-8859-1')
                vtt_content = srt_to_vtt(srt_content).encode('utf-8')
            elif file_extension == ".vtt":
                vtt_content = subtitle_file.read()
            else:
                return ValidationError("Unsupported file extension. Please upload a .srt or .vtt file.") 

            path = settings.MEDIA_ROOT + '/' + subtitle.get_file_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb+') as destination:
                destination.write(vtt_content)
    
        if commit:
            subtitle.save(video_id)
        
        return subtitle
