from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'reqmon.views.index', name='requests'),
    url(r'^updates$', 'reqmon.views.updates', name='requests_updates'),
)
