from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('demo.core.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
