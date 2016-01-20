from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.shortcuts import render
from .models import Requests
import logging
import json
import operator
import re
import time


logger = logging.getLogger(__name__)

REQ_ORDERING = {
    0: 'chronological',
    1: 'reverse',
}

REQ_PRIORITY = {
    0: 'all requests',
    1: '1 or greater',
}


def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


@require_GET
def index(request):
    priority = request.GET.get('priority', '0')
    priority = int(priority) if re.match('^\d+$', priority) else None
    reverse = request.GET.get('reverse', '1')
    reverse = int(reverse) if re.match('^\d+$', reverse) else None

    if priority not in REQ_PRIORITY or reverse not in REQ_ORDERING:
        logger.debug('index GET: %s (pri: %s, rev: %s)' % (request.GET,
                                                           priority,
                                                           reverse))
        return HttpResponseBadRequest()

    requests = Requests.objects.order_by('-id') \
                               .filter(priority__gte=priority)[:10]
    latest = requests[0].id if requests else 0
    requests = sorted(requests,
                      key=operator.attrgetter('id'),
                      reverse=bool(reverse))
    context = {'requests': requests, 'latest': latest,
               'priority': priority, 'reverse': reverse,
               'priorities': REQ_PRIORITY, 'ordering': REQ_ORDERING}

    return render(request, 'reqmon/index.html', context)


@require_GET
def updates(request):
    last = request.GET.get('last', '0')
    last = int(last) if re.match('^\d+$', last) else None
    priority = request.GET.get('priority', '0')
    priority = int(priority) if re.match('^\d+$', priority) else None

    if request.is_ajax() and last is not None and priority in REQ_PRIORITY:
        qs = Requests.objects.order_by('id')
        filter_kwargs = {'pk__gt': last,
                         'priority__gte': priority}
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
        logger.debug('updates GET: %s' % request.GET)
        data = {'result': 'ERROR'}
        return render_to_json_response(data, status=400)
