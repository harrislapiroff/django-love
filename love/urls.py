from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('love.views',
	url(r'^toggle/(?P<content_type_pk>[0-9]+)/(?P<object_pk>[0-9]+)/$', 'toggle_love')
)