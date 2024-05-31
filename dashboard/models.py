from django.db import models
from django.contrib.auth.models import User
ACCESS_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected')
    ]
class MusicFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='music_files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_type = models.CharField(max_length=20, choices=ACCESS_TYPE_CHOICES, default='public')
    allowed_emails = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} uploaded by {self.uploaded_by}"


class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music_file = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPE_CHOICES, default='public')

    def __str__(self):
        return f"{self.user.username} has accesst to {self.music_file.name}"


class Playlist(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    byUser=models.ForeignKey(User, on_delete=models.CASCADE,related_name='byUser')
    files=models.ManyToManyField(MusicFile,related_name='files')


    def __str__(self) -> str:
        return f'{self.name}'


    