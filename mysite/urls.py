from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.login,  name = 'login'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^show$', views.show, name = 'show'),
    url(r'^search$', views.search, name = 'search'),
    url(r'^doreg$', views.doreg, name = 'doreg'),
    url(r'^dolog$', views.dolog, name = 'dolog'),
    url(r'^docmt$', views.docmt, name = 'docmt'),
    url(r'^order$', views.order, name = 'order'),
    url(r'^uinfo$', views.uinfo, name = 'uinfo'),
    url(r'^myorder$', views.myorder, name = 'myorder'),
    url(r'^unorder$', views.unorder, name = 'unorder'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^regok$', views.regok, name = 'regok'),
    url(r'^cmt$', views.cmt, name = 'cmt'),
    url(r'^modemail$', views.modemail, name = 'modemail'),
    url(r'^admin/', include(admin.site.urls)),
)
