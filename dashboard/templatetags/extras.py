from django import template
from dashboard.models import *
from datetime import datetime

register=template.Library()
@register.filter(name='get_files')
def get_files(playlist):
    return playlist.files.all()