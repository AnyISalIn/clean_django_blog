from django.conf.urls import url
from . import views

app_name = 'tag'
urlpatterns = [
    url(r'^$', views.tag_home, name='home'),
]
