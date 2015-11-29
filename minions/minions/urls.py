from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^ajax/suggest$', 'core.views.suggest', name='suggest'),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^convocation/(?P<convocation_id>\d+)$', 'core.views.convocation',
        name='convocation'),

    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
