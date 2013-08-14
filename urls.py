from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Iceblock.views.home', name='home'),
    url(r'^login$', 'Iceblock.views.logggggin', name='login'),
    url(r'^student$', 'Iceblock.views.student', name='student'),
    url(r'^teacher$', 'Iceblock.views.teacher', name='teacher'),
    url(r'^add_class$', 'Iceblock.views.add_class', name='add_class'),
    url(r'^logout_view$', 'Iceblock.views.logout_view', name='logout_view'),
    url(r'^preferences$', 'Iceblock.views.preferences', name='preferences'),
    url(r'^deleted$', 'Iceblock.views.deleted', name='deleted'),
    url(r'^newClassForm$', 'Iceblock.views.newClassForm', name='newClassForm'),
    url(r'^upload$', 'Iceblock.views.upload', name='upload'),
    # url(r'^Iceblock/', include('Iceblock.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
