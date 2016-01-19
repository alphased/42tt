from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render
from .models import Requests
import logging
import json
import re
import time


logger = logging.getLogger(__name__)


def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


def index(request):
    requests = Requests.objects.order_by('id').reverse()[:10]
    return render(request, 'reqmon/index.html', {'requests': requests,
                                                 'latest': requests[0].id})


@require_GET
def updates(request):
    last = request.GET.get('last', '0')
    last = int(last) if re.match('^\d+$', last) else None
    if request.is_ajax() and last is not None:
        qs = Requests.objects.order_by('id')
        filter_kwargs = {'pk__gt': last}
        while True:
            requests = qs.filter(**filter_kwargs)
            if requests:
                break
            else:
                time.sleep(.5)
        latest = requests[len(requests)-1].id if requests else last
        result = [{'timestamp': str(r.timestamp),
                   'method': r.method, 'path': r.path}
                  for r in requests]
        data = {'result': 'OK', 'latest': latest, 'requests': result}
        return render_to_json_response(data)
    else:
        logger.debug('GET: %s' % request.GET)
        data = {'result': 'ERROR'}
        return render_to_json_response(data, status=400)
