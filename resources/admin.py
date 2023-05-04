from django.contrib import admin
from resources.models import ResourceType
from resources.models import ProxyServer
from resources.models import Resources
from django.contrib import admin

@admin.action(description="Mark selected items as enable")
def make_enabled(modeladmin, request, queryset):
    queryset.update(disabled = False)

@admin.action(description="Mark selected items as disabled")
def make_disabled(modeladmin, request, queryset):
    queryset.update(disabled = True)

class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]
    actions = []

class ProxyServerAdmin(admin.ModelAdmin):
    list_display = ["addr", "port", "proxy_type"]
    ordering = ["addr"]
    actions = []

class ResourceAdmin(admin.ModelAdmin):
    list_display = ["type_name", "name", "addr", "port", "proxy_server_info" ,"disabled"]
    ordering = ["name"]
    actions = [make_enabled, make_disabled]
    def type_name(self, obj):
        return obj.type.name
    def proxy_server_info(self, obj):
        if obj.proxy_server:
            return obj.proxy_server.addr + ":" + obj.proxy_server.port + " / " + obj.proxy_server.proxy_type
        else:
            return ""

# Register your models here.
admin.site.register(ResourceType, ResourceTypeAdmin)
admin.site.register(ProxyServer, ProxyServerAdmin)
admin.site.register(Resources, ResourceAdmin)