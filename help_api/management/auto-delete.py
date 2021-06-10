from help_api.models import *
from autofixture import AutoFixture
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Erase data automatically."
    def add_arguments(self, parser):
        parser.add_argument('--c', '--count', type=int)

    def handle(self, *args, **kwargs):
        try:
            count = kwargs['c']
            a = AutoFixture(EntityModel)
            b = AutoFixture(AddressModel)
            c = AutoFixture(ToolsModel)
            d = AutoFixture(SOSModel)

            a.create(count)
            b.create(count)
            c.create(count)
            d.create(count)

        except Exception as e:
            print('Error: {0}', e)
            raise CommandError("Error")