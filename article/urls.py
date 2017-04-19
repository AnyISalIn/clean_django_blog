from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    url(r'(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'(?P<article_id>[0-9]+)/edit$', views.edit, name='edit'),
    url(r'^new/', views.new, name='new')
]
