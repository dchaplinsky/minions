from django.core.management.base import BaseCommand
from elasticsearch_dsl import Index
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections

from core.models import Minion2MP2Convocation
from core.elastic_models import Minion as ElasticMinion


class Command(BaseCommand):
    def handle(self, *args, **options):
        es = connections.get_connection('default')
        Index(ElasticMinion._doc_type.index).delete(ignore=404)
        ElasticMinion.init()

        es.indices.put_settings(
            index=ElasticMinion._doc_type.index,
            body={
                'index.max_result_window': 100000
            }
        )

        counter = 0
        portion = []
        for p in Minion2MP2Convocation.objects.select_related(
                "minion", "mp2convocation", "mp2convocation__mp").all():
            portion.append(ElasticMinion(**p.to_dict()).to_dict(True))
            counter += 1

            if len(portion) >= 100:
                bulk(es, portion)
                portion = []

        bulk(es, portion)

        self.stdout.write(
            'Loaded {} persons to persistence storage'.format(counter))
