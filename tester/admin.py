from django.contrib import admin
from tester.models import TestStage
from django.contrib import admin

@admin.action(description="Mark selected items as enable")
def make_enabled(modeladmin, request, queryset):
    queryset.update(disabled = False)

@admin.action(description="Mark selected items as disabled")
def make_disabled(modeladmin, request, queryset):
    queryset.update(disabled = True)

class TestStageAdmin(admin.ModelAdmin):
    list_display = ["name", "test_command", "display_ok_type", "display_fail_type", "disabled"]
    ordering = ["name"]
    actions = [make_enabled, make_disabled]

# Register your models here.
admin.site.register(TestStage, TestStageAdmin)
