from django.db import models
import uuid
import os
from datetime import datetime
from django.conf import settings

'''
    Fixes the circular import
    I.E. importing resource from video.models
    but then importing user from accounts.models
'''
def get_user_model():
    from accounts.models import User
    return User

class Resource(models.Model):
    AGE_RATING_CHOICES = [
        ('18', '18+'),
        ('15', '15+'),
        ('12', '12+'),
        ('7', '7+'),
        ('unrated', 'Unrated')
    ]
    age_rating = models.CharField(max_length=8, choices=AGE_RATING_CHOICES)

class Video(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('episode', 'Episode'),
        ('clip', 'Clip'),
        ('other', 'Other')
    ]
    uploaded = models.DateTimeField()
    uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False, unique=True)
    extension = models.CharField(max_length=8, default='mp4')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def save(self, *args, **kwargs):
        if self.pk is None: 
            self.uuid = uuid.uuid4()
            self.uploaded = datetime.now()

        super().save(*args, **kwargs)

    # get a movie/episode/clip object, depending on the video type
    def get_attached_obj(self):
        if self.type == 'clip':
            return Clip.objects.filter(video =self.pk).first()
        elif self.type == 'movie':
            return Movie.objects.filter(video=self.pk).first()
        elif self.type == 'episode':
            return Episode.objects.filter(video=self.pk).first()

    def get_resource(self):
        obj = self.get_attached_obj()
        if self.type == 'episode':
            return obj.season.show.resource
        return obj.resource
        
    def get_path(self):
        resource = self.get_resource()
        resource_id = resource.pk
        uuid_path = str(self.uuid).replace('-', '')

        return os.path.join(str(resource_id), f"{uuid_path}{self.extension}")
    
    def get_thumbnail_path(self):
        resource = self.get_resource()
        resource_id = resource.pk
        uuid_path = str(self.uuid).replace('-', '')

        return os.path.join(str(resource_id), f"{uuid_path}.webp")
    
    def get_thumbnail_path(self):
        resource = self.get_resource()
        resource_id = resource.pk
        uuid_path = str(self.uuid).replace('-', '')

        return f'{resource_id}/{uuid_path}.webp'
    
    def __str__(self):
        attached_obj = self.get_attached_obj()
        if attached_obj:
            return attached_obj.get_full_name()
        return "Unknown Full Name"

class Movie(models.Model):
    title = models.CharField(max_length=255)
    video = models.OneToOneField(Video, on_delete=models.CASCADE, primary_key=True)
    lead_actor = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def get_full_name(self):
        return self.title

class Show(models.Model):
    name = models.CharField(max_length=255)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def get_image_path(self):
        return f'{self.resource.id}/image.webp'

class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number = models.PositiveIntegerField()

class Episode(models.Model):
    title = models.CharField(max_length=255)
    season = models.ForeignKey(Season, related_name='episodes', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    description = models.TextField(max_length=2048)

    def get_full_name(self):
        return f"{self.season.show.name} - S{self.season.number}E{self.number} - {self.title}"

class Clip(models.Model):
    title = models.CharField(max_length=255)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def get_full_name(self):
        return self.title

class UserVideoTimestamp(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.PositiveIntegerField()
    last_watched = models.DateTimeField(auto_now=True)

class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    language = models.CharField(max_length=64)
    uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False, unique=True)

    def get_file_path(self):
        resource = self.video.get_resource()
        path = f"{resource.id}/{self.uuid}.vtt"
        return path