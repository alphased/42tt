from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'reqmon.views.index', name='requests'),
)
