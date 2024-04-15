from django.db import models

class Video(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=40, null=True) # does not contain Episode/Season info
    uploaded = models.DateTimeField()

    '''
    the relative path in the media folder
    Example a series will be
    /{entry_id}/{season_id}/{episode_id}/source
    '''
    path = models.CharField(max_length=255)
    AGE_RATING = [
        ('18', '18+'),
        ('15', '15+'),
        ('12', '12+'),
        ('7', '7+'),
        ('unrated', 'Unrated')
    ]
    age_rating = models.CharField(max_length=8, choices=AGE_RATING)
