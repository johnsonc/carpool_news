from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'carpool_news.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('rides.urls', namespace='rides')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^admin/', include(admin.site.urls)),
)
