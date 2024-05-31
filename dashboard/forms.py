from django import forms
from .models import *

class PlaylistCreateForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["name", "files"]

    files = forms.ModelMultipleChoiceField(
        queryset=MusicFile.objects.all(), widget=forms.CheckboxSelectMultiple
    )