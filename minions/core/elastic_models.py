from elasticsearch_dsl import (
    DocType, Completion, Object, Keyword, Text, analyzer, tokenizer,
    Index
)

MINIONS_INDEX = "minions"
minions_idx = Index(MINIONS_INDEX)

namesAutocompleteAnalyzer = analyzer(
    'namesAutocompleteAnalyzer',
    tokenizer=tokenizer(
        'autocompleteTokenizer',
        type='edge_ngram',
        min_gram=2,
        max_gram=20,
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
        search_analyzer="namesAutocompleteSearchAnalyzer"
    )
    all = Text(analyzer='ukrainian')
