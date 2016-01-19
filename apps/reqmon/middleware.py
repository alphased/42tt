from reqmon.models import Requests
from django.core.urlresolvers import reverse


class RequestsMiddleware():

    def process_request(self, request):
        if reverse('requests_updates') != request.path:
            Requests.objects.create(path=request.path, method=request.method)
        return None
