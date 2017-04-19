from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from article import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^article/', include('article.urls')),
    url(r'^author/', include('author.urls', namespace='author')),
    url(r'^tag/', include('tag.urls', namespace='tag')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
handler404 = 'clean_django_blog.views.page404'
