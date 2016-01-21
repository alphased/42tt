MANAGE=django-admin.py
SETTINGS=fortytwo_test_task.settings

PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$SETTINGS $MANAGE enummodel 2> `date -I`.dat