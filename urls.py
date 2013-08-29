from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'IceblockGit.views.home', name='home'),
    url(r'^login$', 'IceblockGit.views.logggggin', name='login'),
    url(r'^student$', 'IceblockGit.views.student', name='student'),
    url(r'^teacher$', 'IceblockGit.views.teacher', name='teacher'),
    url(r'^add_class$', 'IceblockGit.views.add_class', name='add_class'),
    url(r'^logout_view$', 'IceblockGit.views.logout_view', name='logout_view'),
    url(r'^preferences$', 'IceblockGit.views.preferences', name='preferences'),
    url(r'^deleted$', 'IceblockGit.views.deleted', name='deleted'),
    url(r'^newClassForm$', 'IceblockGit.views.newClassForm', name='newClassForm'),
    url(r'^upload$', 'IceblockGit.views.upload', name='upload'),
    url(r'^Generator$', 'IceblockGit.views.Generator', name='Generator'),
    url(r'^About$', 'IceblockGit.views.About', name='About'),
    url(r'^Register$', 'IceblockGit.views.Register', name='Register'),
    url(r'^showassignments$', 'IceblockGit.views.showassignments', name='showassignments'),  
    # url(r'^IceblockGit/', include('IceblockGit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
