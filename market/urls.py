from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gifts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'market.views.splash', name='splash'),
    url(r'^our-philosophy/$', 'market.views.philosophy', name='philosophy'),
    url(r'^join/$', 'market.views.join', name='join'),
    url(r'^privacy/$', 'market.views.privacy', name='privacy'),
    url(r'^terms-of-service/$', 'market.views.tos', name='tos'),
    url(r'^login/$', 'market.views.login', name='login'),
    url(r'^signup/$', 'market.views.signup', name='signup'),
    url(r'^confirmation/(?P<ref>[A-Za-z0-9]{8})$', 'market.views.confirmation', name='confirmation'),
    (r'^django-rq/', include('django_rq.urls')),

)
