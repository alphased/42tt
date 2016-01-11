from django.shortcuts import render
from .models import User


def home(request):
    '''Display user profile

    Based on the task description, assume that the profile being displayed
    is always for user 'admin'
    '''
    profile = User.objects.get(username='admin')
    return render(request, 'hello/index.html', {'profile': profile})
