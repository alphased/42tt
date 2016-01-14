from reqmon.models import Requests


class RequestsMiddleware():

    def process_request(self, request):
        Requests.objects.create(path=request.path, method=request.method)
