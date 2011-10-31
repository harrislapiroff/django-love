from django.db import models
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from love.models import Love
from love.forms import ToggleLoveForm


@csrf_protect
@require_POST
def toggle_love(request, next=None):
	"""
	Toggle love.
	
	"""
	
	data = request.POST.copy()
    
	next = data.get("next", next)
	content_type = data.get("content_type")
	object_pk = data.get("object_pk")
	
	if content_type == None or object_pk == None:
		return LoveBadRequest("No object specified.")
		
	try:
		model = models.get_model(*content_type.split(".", 1))
		target = model.objects.get(pk=object_pk)
	except:
		return LoveBadRequest("An error occured trying to get the target object.")
	
	form = ToggleLoveForm(target, data=data)
	
	if form.security_errors():
		return LoveBadRequest("Form failed security verification:" % escape(str(form.security_errors())))
	
	# first filter on the object itself
	filters = form.get_filter_kwargs()
	
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
	if target.get_absolute_url is not None:
		return HttpResponseRedirect(target.get_absolute_url())
	
	# faling both of those, return a 404
	raise Http404('next not passed to view and get_absolute_url not defined on object')