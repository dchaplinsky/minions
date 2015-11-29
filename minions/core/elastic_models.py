from elasticsearch_dsl import DocType, Completion


class Minion(DocType):
    """Person document."""
    name_suggest = Completion(preserve_separators=False)
    mp_name_suggest = Completion(preserve_separators=False)

    class Meta:
        index = 'minions'
