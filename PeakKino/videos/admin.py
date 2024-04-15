from django.contrib import admin
from django.db import models
from .models import *

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'age_rating')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded')
    readonly_fields = ('uuid',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('video', 'lead_actor', 'director')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource')

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'season', 'video')
    search_fields = ('title', 'season__name')

admin.site.register(Clip)