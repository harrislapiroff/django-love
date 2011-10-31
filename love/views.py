from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from love.models import Love


class LoveBadRequest(HttpResponseBadRequest):
	pass


def toggle_love(request, content_type_pk=None, object_pk=None):
	
	next = None if 'next' not in request.GET else request.GET['next']
	
	if content_type_pk == None or object_pk == None:
		return LoveBadRequest
	
	content_type = ContentType.objects.get(pk=content_type_pk)
	obj = get_object_or_404(content_type.model_class(), pk=object_pk)
	
	# first filter on the object itself
	filters = {'content_type': content_type, 'object_pk': object_pk}
	
	# either add a user or a session key to our list of filters
	if request.user.is_authenticated():
		filters['user'] = request.user
	else:
		filters['session_key'] = request.session.session_key
	
	# if it exists, delete it; if not, create it.
	try:
		love = Love.objects.get(**filters)
		love.delete()
	except Love.DoesNotExist:
		love = Love(**filters)
		love.save()
	
	# if a next url is set, redirect there
	if next:
		return HttpResponseRedirect(next)
	
	# if not, redirect to the original object's permalink
	if obj.get_absolute_url is not None:
		return HttpResponseRedirect(obj.get_absolute_url())
	
	# faling both of those, return a 404
	raise Http404('next not passed to view in querystring and get_absolute_url not defined on object')