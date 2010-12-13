from django.contrib import admin

from netauth.models import NetID


class NetIDAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'identity']

admin.site.register(NetID, NetIDAdmin)
