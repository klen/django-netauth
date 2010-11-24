from django.contrib import admin

from publicauth.models import PublicID


class PublicIDAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'identity']
admin.site.register(PublicID, PublicIDAdmin)

