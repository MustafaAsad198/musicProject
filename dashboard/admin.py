from django.contrib import admin
from .models import MusicFile,Access,Playlist
from django.contrib import admin
# Register your models here.

class MusicAdmin(admin.ModelAdmin):
    list_display = ('name','file','uploaded_by','upload_type','allowed_emails')

class AccessAdmin(admin.ModelAdmin):
    list_display = ('user','music_file','access_type')
admin.site.register(MusicFile,MusicAdmin)
admin.site.register(Access,AccessAdmin)
admin.site.register(Playlist)