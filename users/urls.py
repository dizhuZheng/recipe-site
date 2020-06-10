from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>\w+)/change/$', views.change_profile, name='change_profile'),
    url(r'^my_saves/(?P<username>\w+)/$', views.my_saves, name='my_saves'),
    url(r'^my_posts/(?P<username>\w+)/$', views.my_posts, name='my_posts'),
    url(r'^my_drafts/', views.my_drafts, name='my_drafts'),
    url(r'^search/', views.search_index, name='search'),
]
