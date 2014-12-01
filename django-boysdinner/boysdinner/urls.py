from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles import views

from django.contrib import admin
admin.autodiscover()
from boysdinner import views

urlpatterns = [
    #boysdinner root/index page: enter name, enter dish name
	#presumably is skipped if session still active
	#date identifies the dinner
    url(r'^(?P<first_name>\w+)/(?P<dish_name>\w+)/$', views.signin, name='signin'),
    url(r'^signin/$', views.signin, name='signin'),

	#on signin page allows user to search for their record
	#for eventual updating of name and and/or dish name
    url(r'^search/$', views.search_person, name='search_person'),

	#logs in proceeds to vote page where program checks to
	#see if someone has submitted to be voted upon and if yes
	# puts form at top or shows "error style" message and shows
	#all votes that user has made so far below
    url(r'^boysdinner/(?P<voter_id>\d+)/vote/$', views.vote, name='vote'),

    #processes updates to old votes prefixed forms
    url(r'^boysdinner/(?P<voter_id>\d+)/(?P<pre_fix>\d+)/old_votes/$', views.old_votes, name='old_votes'),

	#overall totals in a chart per person-name in descending order
	#so that 1st place comes first, etc
    url(r'^boysdinner/(?P<voter_id>\d+)/results/$', views.results, name='results'),

	##displays others' votes for me, per person including comments
    #url(r'^(?P<user_id>\d+/votesforme/$', views.votesforme, name='votesforme'),

] 

urlpatterns += staticfiles_urlpatterns()
