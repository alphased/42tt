from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', 'hello.views.home', name='home'),
    url(r'^requests/', include('reqmon.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
