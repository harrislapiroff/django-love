from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Love(models.Model):
	"A user or session owned indication of love for some object. Either user or session should be present to indicate the owner."
	content_type = models.ForeignKey(ContentType)
	object_pk = models.TextField(max_length=255)
	content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
	user = models.ForeignKey(User, null=True, blank=True)
	session_key = models.TextField(max_length=255, null=True, blank=True)
	added_date = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.content_object.__unicode__()
	
	class Meta:
		unique_together = ('content_type', 'object_pk', 'user', 'session_key')