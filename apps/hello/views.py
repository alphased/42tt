from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import User

import logging
logger = logging.getLogger(__name__)

DEFAULT_USER_PROFILE = {
    "username": "admin",
    "first_name": "Andrii",
    "last_name": "Ilika",
    "birthday": "1980-11-14",
    "bio": "Parchment then, is that your holy well,\r\n"
           "from which drink always slakes your thirst?\r\n"
           "You'll never truly be refreshed until\r\n"
           "It pours itself from your own soul, first.",
    "email": "alphasedout@gmail.com",
    "contact_jabber": "alphased@khavr.com",
    "contact_skype": "ai22-uanic",
    "othercontacts": "Enough is enough",
}


def home(request):
    '''Display 'admin' user profile

    Based on the task description, assume that the profile being displayed
    is always for user 'admin'
    '''
    logger.debug('request user: %s' % request.user)
    profile = User(**DEFAULT_USER_PROFILE)
    try:
        profile = User.objects.get(username='admin')
    except ObjectDoesNotExist as e:
        logger.warning(e)
    logger.info('using profile: %s' % profile)

    return render(request, 'hello/index.html', {'profile': profile})
