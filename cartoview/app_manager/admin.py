from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from django.contrib import admin
from future import standard_library
from .installer import AppInstaller
from .models import App, AppInstance, AppStore, AppType
from .utils import populate_apps
standard_library.install_aliases()


def uninstall_selected(modeladmin, request, queryset):
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied
    for app in queryset:
        try:
            app_store = app.store.id if app.store else None
            installer = AppInstaller(
                app.name, store_id=app_store, user=request.user)
            installer.uninstall()
        except Exception as e:
            return HttpResponseServerError(e.message)


uninstall_selected.short_description = "Uninstall Selected Apps"


def suspend_selected(modeladmin, request, queryset):
    for app in queryset:
        try:
            app.set_active(False)
        except Exception as e:
            return HttpResponseServerError(e.message)
    populate_apps()


suspend_selected.short_description = "Suspend Selected Apps"


def activate_selected(modeladmin, request, queryset):
    for app in queryset:
        try:
            app.set_active()
        except Exception as e:
            return HttpResponseServerError(e.message)
    populate_apps()


activate_selected.short_description = "Activate Selected Apps"


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    ordering = ('order', )
    actions = [uninstall_selected, suspend_selected, activate_selected]


admin.site.register(AppType)
admin.site.register(AppInstance)
admin.site.register(AppStore)
