from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^ajax/suggest$', 'core.views.suggest', name='suggest'),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^search$', 'core.views.search', name='search'),
    url(r'^mp/(?P<mp_id>\d+)$', 'core.views.mp_details',
        name='mp_details'),
    url(r'^minion/(?P<minion_id>\d+)$', 'core.views.minion_details',
        name='minion_details'),
    url(r'^convocation/(?P<convocation_id>\d+)$', 'core.views.convocation',
        name='convocation'),

    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.handler404"
