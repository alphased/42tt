from reqmon.models import Requests
from django.core.urlresolvers import reverse


SKIP_PATH = [reverse('requests_updates'), ]
PRI1_PATH = [reverse('admin:index'), ]


class RequestsMiddleware():

    def process_request(self, request):
        if request.path in SKIP_PATH:
            return None

        request_kwargs = {}
        if request.method == 'POST':
            request_kwargs['priority'] = 1
        elif request.path in PRI1_PATH:
            request_kwargs['priority'] = 1

        Requests.objects.create(path=request.path,
                                method=request.method,
                                **request_kwargs)
