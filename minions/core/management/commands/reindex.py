from django.core.management.base import BaseCommand
from elasticsearch_dsl import Index

from core.models import Minion2MP2Convocation
from core.elastic_models import Minion as ElasticMinion


class Command(BaseCommand):
    def handle(self, *args, **options):
        Index(ElasticMinion._doc_type.index).delete(ignore=404)

        ElasticMinion.init()
        counter = 0
        for p in Minion2MP2Convocation.objects.select_related(
                "minion", "mp2convocation", "mp2convocation__mp").all():
            item = ElasticMinion(**p.to_dict())
            item.save()
            counter += 1

        self.stdout.write(
            'Loaded {} persons to persistence storage'.format(counter))
