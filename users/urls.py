# users/urls.py

from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/change/$', views.change_profile, name='change_profile'),
    url(r'^my_saves/$', views.my_saves, name='my_saves'),
    url(r'^my_posts/$', views.my_posts, name='my_posts'),
    url(r'^my_drafts/$', views.my_drafts, name='my_drafts'),
]
