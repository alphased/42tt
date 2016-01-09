from django.conf.urls import patterns, include, url

from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # from django.views.generic.base import TemplateView
    url(r'^$', TemplateView.as_view(template_name='hello/index.html')),

    url(r'^admin/', include(admin.site.urls)),
)
