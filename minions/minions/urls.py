from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core.models import Convocation, MemberOfParliament, Minion
from core import views as core_views

urlpatterns = [
    url(r'^ajax/suggest$', core_views.suggest, name='suggest'),
    url(r'^$', core_views.home, name='home'),
    url(r'^search$', core_views.search, name='search'),
    url(r'^mp/(?P<mp_id>\d+)$', core_views.mp_details,
        name='mp_details'),
    url(r'^minion/(?P<minion_id>\d+)$', core_views.minion_details,
        name='minion_details'),
    url(r'^convocation/(?P<convocation_id>\d+)$', core_views.convocation,
        name='convocation'),

    url(r'^sitemap\.xml$', sitemap, {
        'sitemaps': {
            "convocations": GenericSitemap({
                'queryset': Convocation.objects.all()
            }),
            "mps": GenericSitemap({
                'queryset': MemberOfParliament.objects.all()
            }),
            "minions": GenericSitemap({
                'queryset': Minion.objects.all()
            }),
        }},
        name='django.contrib.sitemaps.views.sitemap'),

    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),

    # Нехай щастить!
    # url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = core_views.handler404
