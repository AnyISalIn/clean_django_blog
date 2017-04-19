from django.shortcuts import render
from .models import Tag


def tag_home(request):
    tags = Tag.objects.all()
    return render(request, 'tag.html', {'tags': tags})
