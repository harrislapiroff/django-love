from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('love.views',
	url(r'^toggle/$', 'toggle_love', name="love-toggle")
)