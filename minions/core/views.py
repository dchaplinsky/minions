from operator import itemgetter
from collections import Counter
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Count
from django.views import View

from elasticsearch_dsl.query import Q
from elasticsearch_dsl import MultiSearch

from core.elastic_models import Minion as ElasticMinion
from core.models import (
    Convocation, Minion, MemberOfParliament, MP2Convocation,
    Minion2MP2Convocation)
from core.paginator import paginated, DjangoPageRangePaginator


class SuggestView(View):
    def get(self, request):
        q = request.GET.get('q', '').strip()

        suggestions = []
        seen = set()

        s = ElasticMinion.search().source(
            ['names_autocomplete']
        ).highlight('names_autocomplete').highlight_options(
            order='score', fragment_size=100,
            number_of_fragments=10,
            pre_tags=['<strong>'],
            post_tags=["</strong>"]
        )

        s = s.query(
            "bool",
            must=[
                Q(
                    "match",
                    names_autocomplete={
                        "query": q,
                        "operator": "and"
                    }
                )
            ],
            should=[
                Q(
                    "match_phrase",
                    names_autocomplete__raw={
                        "query": q,
                        "boost": 2
                    },
                ),
                Q(
                    "match_phrase_prefix",
                    names_autocomplete__raw={
                        "query": q,
                        "boost": 2
                    },
                )
            ]
        )[:200]

        res = s.execute()

        for r in res:
            if "names_autocomplete" in r.meta.highlight:
                for candidate in r.meta.highlight["names_autocomplete"]:
                    if candidate.lower() not in seen:
                        suggestions.append(candidate)
                        seen.add(candidate.lower())


        rendered_result = [
            render_to_string("autocomplete.jinja", {
                "result": {
                    "hl": k
                }
            })
            for k in suggestions[:20]
        ]

        return JsonResponse(rendered_result, safe=False)


def home(request):
    return render(request, "home.jinja", {
        "count_of_minions": Minion2MP2Convocation.objects.count(),
        "convocations": Convocation.objects.order_by("-number").annotate(
            num_mps=Count('mp2convocation', distinct=True),
            num_minions=Count('mp2convocation__minion'))
    })


def convocation(request, convocation_id):
    conv = get_object_or_404(Convocation.objects.annotate(
        num_mps=Count('mp2convocation', distinct=True),
        num_minions=Count('mp2convocation__minion')),
        number=int(convocation_id))

    letter = request.GET.get("letter", False)

    mps = MP2Convocation.objects.select_related("mp").filter(
        convocation=conv).order_by("mp__name").extra(
        select={'first_letter': "SUBSTR(core_memberofparliament.name, 1, 1)"})

    alphabet = MP2Convocation.objects.select_related("mp").filter(
        convocation=conv).order_by("mp__name").extra(
            select={
                'first_letter': "SUBSTR(core_memberofparliament.name, 1, 1)"
            }
        ).values_list('first_letter', flat=True)

    if letter not in alphabet:
        letter = False

    if letter:
        mps = mps.filter(mp__name__startswith=letter)

    return render(request, "convocation.jinja", {
        "convocation": conv,
        "alphabet": Counter(map(str.upper, alphabet)),
        "current_letter": letter,
        "mps": paginated(request, mps, DjangoPageRangePaginator),
    })


def search(request):
    query = request.GET.get("q", "")

    if query:
        persons = ElasticMinion.search().query(
            "multi_match", query=query,
            operator="and",
            fields=["mp.name", "name", "persons"])
    else:
        persons = ElasticMinion.search().query('match_all')

    return render(request, "search.jinja", {
        "minions": paginated(
            request, persons.sort('mp.grouper', '-paid', 'name.raw'), cnt=30),
        "q": query
    })


def mp_details(request, mp_id):
    return render(request, "mp.jinja", {
        "mp": get_object_or_404(MemberOfParliament, pk=int(mp_id))
    })


def minion_details(request, minion_id):
    return render(request, "minion.jinja", {
        "minion": get_object_or_404(Minion, pk=int(minion_id))
    })


def handler404(request, exception):
    response = render_to_string('404.jinja')
    return HttpResponseNotFound(
        response, content_type="text/html"
    )
