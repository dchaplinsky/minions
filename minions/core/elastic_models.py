from elasticsearch_dsl import (
    DocType, Completion, Object, Keyword, Text, analyzer, tokenizer,
    Index
)

MINIONS_INDEX = "minions"
minions_idx = Index(MINIONS_INDEX)
minions_idx.settings(
    number_of_replicas=0
)

namesAutocompleteAnalyzer = analyzer(
    'namesAutocompleteAnalyzer',
    tokenizer=tokenizer(
        'autocompleteTokenizer',
        type='edge_ngram',
        min_gram=1,
        max_gram=25,
        token_chars=[
            'letter',
            'digit'
        ]
    ),
    filter=[
        "lowercase"
    ]
)
namesAutocompleteSearchAnalyzer = analyzer(
    'namesAutocompleteSearchAnalyzer',
    tokenizer=tokenizer("lowercase")
)

minions_idx.analyzer(namesAutocompleteAnalyzer)
minions_idx.analyzer(namesAutocompleteSearchAnalyzer)


@minions_idx.doc_type
class Minion(DocType):
    """Person document."""

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

    persons = Text(analyzer='ukrainian', copy_to="all")
    companies = Text(analyzer='ukrainian', copy_to="all")

    names_autocomplete = Text(
        analyzer='namesAutocompleteAnalyzer',
        search_analyzer="namesAutocompleteSearchAnalyzer",
        fields={'raw': Text(index=True)}
    )
    all = Text(analyzer='ukrainian')

    class Meta:
        index = MINIONS_INDEX
        doc_type = "minions_minions_doctype"
