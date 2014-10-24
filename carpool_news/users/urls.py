from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^login$', 'users.views.login', name='login'),
    url(r'^logout$', 'users.views.logout', name='logout'),
    url(r'^profile$', 'users.views.profile', name='profile'),
    url(r'^register$', 'users.views.register', name='register'),
)
