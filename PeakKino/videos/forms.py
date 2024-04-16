from django import forms
from django.conf import settings
from .models import Clip, Resource, Video
from django.core.exceptions import ValidationError
import os

class ClipUploadForm(forms.ModelForm):
    class Meta:
        model = Clip
        fields = ['title', 'resource_age_rating']

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

        self.handle_uploaded_file(uploaded_file, video)
        return clip
    
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
