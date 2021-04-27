from django.db import models

# Create your models here.
class Songs(models.Model):
    # song title
    title = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artist = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)

class MyFile(models.Model):

    resume = models.FileField(blank=False, null=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)