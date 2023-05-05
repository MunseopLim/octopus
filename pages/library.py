from django.template.defaultfilters import register
from tester.models import TestStage


@register.filter(name="display_danger_color_if_contains_fail")
def display_danger_color_if_contains_fail(str):
    if "Fail" in str:
        # bootstrap
        return "text-danger"
    else:
        return ""


@register.filter(name="get_resume_command")
def get_resume_command(stage_name):
    print("[pages.library.get_resume_command] stage_name: " + stage_name)
    try:
        stage = TestStage.objects.get(name=stage_name)
        print("[pages.library.get_resume_command] stage: " + str(stage))
        return stage.resume_command
    except Exception as e:
        print("[pages.library.get_resume_command] error: " + str(e))
        return ""


@register.filter(name="select_by_name")
def select_by_name(d, k):
    return d.get(k)


@register.simple_tag
def nav_active(pos, param):
    if pos == param:
        return "active"
    else:
        return ""
