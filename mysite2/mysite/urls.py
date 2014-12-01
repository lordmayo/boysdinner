from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'mysite.views.home'),
	url(r'^polls/', include('polls.urls', namespace="polls")),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^boysdinner/', include('boysdinner.urls', namespace="boysdinner")),
)
