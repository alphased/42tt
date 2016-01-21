from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    args = ''
    help = 'Prints all project models and the their object count'

    def handle(self, *args, **options):
        for conttype in ContentType.objects.all():
            model = conttype.model_class()
            module = model.__module__
            modelname = model.__name__
            count = model._default_manager.count()
            output = '%s.%s %d' % (module, modelname, count)
            self.stdout.write(output)
            self.stderr.write('%s%s' % ('error: ', output))
