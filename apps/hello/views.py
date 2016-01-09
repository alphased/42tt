from django.shortcuts import render


def home(request):
    '''
    from django.views.generic.base import TemplateView
    url(r'^$', TemplateView.as_view(template_name='hello/index.html')),
    '''
    return render(request, 'hello/index.html')
