from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'rides.views.index', name='index'),
)
