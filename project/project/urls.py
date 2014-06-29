from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='index'),
    url(r'^api/', include('app.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

# # works if DEBUG is True only
# # - for apps static files
urlpatterns += staticfiles_urlpatterns()
# # - for static files directory
urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
