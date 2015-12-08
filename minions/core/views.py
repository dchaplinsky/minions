from operator import itemgetter
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum

from core.elastic_models import Minion as ElasticMinion
from core.models import Convocation, Minion, MemberOfParliament
from core.paginator import paginated, DjangoPageRangePaginator


def suggest(request):
    def assume(q, fuzziness):
        results = []

        search = ElasticMinion.search()\
            .suggest(
                'name',
                q,
                completion={
                    'field': "name_suggest",
                    'size': 10,
                    'fuzzy': {
                        'fuzziness': fuzziness,
                        'unicode_aware': 1
                    }
                }
        )

        res = search.execute()
        if res.success:
            results += res.suggest['name'][0]['options']

        search = ElasticMinion.search()\
            .suggest(
                'name',
                q,
                completion={
                    'field': "mp_name_suggest",
                    'size': 10,
                    'fuzzy': {
                        'fuzziness': fuzziness,
                        'unicode_aware': 1
                    }
                }
        )

        res = search.execute()
        if res.success:
            results += res.suggest['name'][0]['options']

        results = sorted(results, key=itemgetter("score"), reverse=True)

        if results:
            return [val['text'] for val in results]
        else:
            []

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
        "convocations": Convocation.objects.order_by("-number").annotate(
            num_mps=Count('mp2convocation', distinct=True),
            num_minions=Count('mp2convocation__minion'))
    })


def convocation(request, convocation_id):
    conv = get_object_or_404(Convocation.objects.annotate(
        num_mps=Count('mp2convocation', distinct=True),
        num_minions=Count('mp2convocation__minion')),
        number=int(convocation_id))

    minions = Minion.objects.select_related("mp").filter(
        mp__convocation=conv).order_by("mp")

    return render(request, "listing.jinja", {
        "convocation": conv,
        "minions": paginated(request, minions, DjangoPageRangePaginator)
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
        "minions": paginated(request, persons.sort('mp.name')),
        "q": query
    })


def mp_details(request, mp_id):
    return render(request, "mp.jinja", {
        "mp": get_object_or_404(MemberOfParliament, pk=int(mp_id))
    })
