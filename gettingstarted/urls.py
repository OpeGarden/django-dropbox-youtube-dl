from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
	url(r'^status', hello.views.status, name='status'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^latestUsed', hello.views.latestUsed, name='latestUsed'),
    url(r'^slots', hello.views.slots, name='slots'),
    url(r'^admin/', include(admin.site.urls)),

)
