from operator import itemgetter
from collections import Counter
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from core.elastic_models import Minion as ElasticMinion
from core.models import (
    Convocation, Minion, MemberOfParliament, MP2Convocation,
    Minion2MP2Convocation)
from core.paginator import paginated, DjangoPageRangePaginator


def unique(source):
    """
    Returns unique values from the list preserving order of initial list.
    :param source: An iterable.
    :type source: list
    :returns: List with unique values.
    :rtype: list
    """
    seen = set()
    return [seen.add(x) or x for x in source if x not in seen]


def suggest(request):
    def assume(q, fuzziness):
        results = []

        search = ElasticMinion.search()\
            .source(['name_suggest', 'name'])\
            .params(size=0)\
            .suggest(
                'name',
                q,
                completion={
                    'field': "name_suggest",
                    'size': 10,
                    'fuzzy': {
                        'fuzziness': fuzziness,
                        'unicode_aware': True
                    }
                }
        )

        res = search.execute()
        if res.success:
            results += res.suggest['name'][0]['options']

        search = ElasticMinion.search()\
            .source(['mp_name_suggest', 'mp.name'])\
            .params(size=0)\
            .suggest(
                'name',
                q,
                completion={
                    'field': "mp_name_suggest",
                    'size': 10,
                    'fuzzy': {
                        'fuzziness': fuzziness,
                        'unicode_aware': True
                    }
                }
        )

        res = search.execute()
        if res.success:
            results += res.suggest['name'][0]['options']

        results = sorted(results, key=itemgetter("_score"), reverse=True)

        if results:
            return unique(
                val._source.name
                if "name" in val._source else val._source.mp.name
                for val in results
            )
        else:
            return []

    q = request.GET.get('q', '').strip()

    # It seems, that for some reason 'AUTO' setting doesn't work properly
    # for unicode strings
    fuzziness = 0

    if len(q) > 2:
        fuzziness = 1

    suggestions = assume(q, fuzziness)

    if not suggestions:
        suggestions = assume(q, fuzziness + 1)

    return JsonResponse(suggestions, safe=False)


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
            fields=["mp.name", "name"])
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


def handler404(request):
    response = render(request, '404.jinja')
    response.status_code = 404
    return response
