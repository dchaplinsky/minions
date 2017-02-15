from elasticsearch_dsl import (
    DocType, Completion, Object, Keyword, Text)


class Minion(DocType):
    """Person document."""
    name_suggest = Completion(preserve_separators=False)
    mp_name_suggest = Completion(preserve_separators=False)
    paid = Keyword(index=False)
    name = Text(
        index=True, analyzer='ukrainian',
        fields={'raw': Keyword(index=True)}
    )
    mp = Object(
        properties={
            "grouper": Keyword(index=False),
            "name": Text(
                index=True, analyzer='ukrainian',
                fields={'raw': Keyword(index=True)}
            )
        }
    )

    class Meta:
        index = 'minions'
