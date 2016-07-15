from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

import xadmin
xadmin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tsrm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(xadmin.site.urls)),
)
