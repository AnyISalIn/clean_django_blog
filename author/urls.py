from django.conf.urls import url
from . import views

app_name = 'author'
urlpatterns = [
    url(r'^register/', views.register_view, name='register'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout')
]
