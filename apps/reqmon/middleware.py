from reqmon.models import Requests
from django.conf import settings


# Need for speed
SKIP_PATH = [str(url) for url in settings.SKIP_PATH]
PRI1_PATH = [str(url) for url in settings.PRI1_PATH]


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
