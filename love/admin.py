from django.contrib import admin
from love.models import Love

class LoveAdmin(admin.ModelAdmin):
	pass

admin.site.register(Love, LoveAdmin)