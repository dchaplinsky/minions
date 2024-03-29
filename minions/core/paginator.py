from django.core.paginator import Paginator, Page
from django.conf import settings

from elasticsearch_dsl.response import Response


class AbstractPage(Page):
    @property
    def contextual_page_range(self):
        """Determines a list of page numbers based on current page and total
        number of pages. Includes one page to each side of the current one or
        two to the side at edges.

        Taken and adapted from:
        https://gist.github.com/tomchristie/321140cebb1c4a558b15"""
        current = self.number
        final = self.paginator.num_pages

        # If it's small enough - just show them all
        if final <= 5:
            return self.paginator.page_range

        # We always include the first two pages, last two pages, and
        # two pages either side of the current page.
        included = set((
            1,
            current - 1, current, current + 1,
            final
        ))

        # If the break would only exclude a single page number then we
        # may as well include the page number instead of the break.
        if current <= 4:
            included.add(2)
            included.add(3)
        if current >= final - 3:
            included.add(final - 1)
            included.add(final - 2)

        # Now sort the page numbers and drop anything outside the limits.
        included = [
            idx for idx in sorted(list(included))
            if idx > 0 and idx <= final
        ]

        # Finally insert any `...` breaks
        if current > 4:
            included.insert(1, None)
        if current < final - 3:
            included.insert(len(included) - 1, None)
        return included


class ElasticPage(AbstractPage):
    def __len__(self):
        return self.paginator.count

    def __getitem__(self, index):
        if not isinstance(index, (slice, int)):
            raise TypeError
        # The object_list is converted to a Response so that its result can be
        # used as a normal iterable. Doesn't trigger more than one hit too.
        if not isinstance(self.object_list, Response):
            self.object_list = self.object_list.execute()
        return self.object_list[index]


class ElasticPageRangePaginator(Paginator):
    """Implementation of Django's Paginator that makes amends for
    Elasticsearch DSL search object details. Pass a search object to the
    constructor as `object_list` parameter."""
    def _get_page(self, *args, **kwargs):
        return ElasticPage(*args, **kwargs)


class DjangoPageRangePaginator(Paginator):
    """Implementation of Django's Paginator that makes amends for
    Elasticsearch DSL search object details. Pass a search object to the
    constructor as `object_list` parameter."""
    def _get_page(self, *args, **kwargs):
        return AbstractPage(*args, **kwargs)


def paginated(request, search, klass=ElasticPageRangePaginator,
              cnt=settings.CATALOG_PER_PAGE):
    """Helper function that handles common pagination pattern."""
    paginator = klass(search, cnt)
    page = request.GET.get('page', 1)
    return paginator.page(page)
