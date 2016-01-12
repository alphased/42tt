from django.shortcuts import render
from .models import User

import logging
logger = logging.getLogger(__name__)


def home(request):
    '''Display 'admin' user profile

    Based on the task description, assume that the profile being displayed
    is always for user 'admin'
    '''
    logger.debug('request user: %s' % request.user)
    profile = None
    try:
        profile = User.objects.get(username='admin')
    except ObjectDoesNotExist as e:
        logger.warning(e)
    logger.info('using profile: %s' % profile)

    return render(request, 'hello/index.html', {'profile': profile})
