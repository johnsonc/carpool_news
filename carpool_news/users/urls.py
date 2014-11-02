from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^login$', 'users.views.login', name='login'),
    url(r'^logout$', 'users.views.logout', name='logout'),
    url(r'^register$', 'users.views.register', name='register'),
    url(
        r'^routes$',
        'users.views.list_user_routes',
        name='list_user_routes'),
    url(
        r'^delete_user_route/(?P<id>\d+)$',
        'users.views.delete_user_route',
        name='delete_user_route'),
    url(
        r'^create_user_route$',
        'users.views.create_user_route',
        name='create_user_route')
)
