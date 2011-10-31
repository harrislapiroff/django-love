from django.contrib import admin
from love.models import Love

class LoveAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'user', 'session_key', 'added_date')
	readonly_fields = ('__unicode__', 'content_type', 'object_pk', 'user', 'session_key')
	fieldsets = ((None, {
		'fields': (('__unicode__',), ('content_type', 'object_pk'), ('user', 'session_key'),)
	}),)

admin.site.register(Love, LoveAdmin)