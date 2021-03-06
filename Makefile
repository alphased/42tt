MANAGE=django-admin.py
SETTINGS=fortytwo_test_task.settings

# test:
# 	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) test
# 	flake8 --exclude '*migrations*' apps fortytwo_test_task

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) test
	flake8 --exclude '*migrations*' apps fortytwo_test_task

coverage:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) coverage run --source=apps --branch manage.py test
	flake8 --exclude '*migrations*' apps fortytwo_test_task

shell:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) shell

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) syncdb --noinput

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate

collectstatic:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) collectstatic --noinput

.PHONY: test coverage shell run syncdb migrate collectstatic
