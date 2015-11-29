from django.core.management.base import BaseCommand
from core.models import Minion
from core.elastic_models import Minion as ElasticMinion


class Command(BaseCommand):
    def handle(self, *args, **options):

        ElasticMinion.init()
        counter = 0
        for p in Minion.objects.select_related("mp").all():
            item = ElasticMinion(**p.to_dict())
            item.save()
            counter += 1

        self.stdout.write(
            'Loaded {} persons to persistence storage'.format(counter))
