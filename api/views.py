from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
from pages.target import target
from resources.models import Resources
from api.thread_task import thread_task
import json


# Create your views here.
def request(request):
    status = 500
    if request.method == "POST":
        print("[api.views.request] begin: " + str(datetime.now()))
        jsonObj = json.loads(request.body)[0]
        print(
            "[api.views.request] sig: "
            + str(request.session._session_key)
            + ", command: "
            + jsonObj["command"]
            + ", target: "
            + jsonObj["target"]
        )
        task = thread_task(
            request.session._session_key, jsonObj["command"], jsonObj["target"]
        )
        result_dict = task.command_execute()
        print("[api.views.request] result: " + str(result_dict))
        print("[api.views.request] end: " + str(datetime.now()))
        return JsonResponse(result_dict)
    return HttpResponse(status=status)


def disabled_resource(request):
    status = 500
    if request.method == "POST":
        print("[api.views.disabled_resource] begin: " + str(datetime.now()))
        jsonObj = json.loads(request.body)[0]
        print("[api.views.disabled_resource] jsonObj: " + str(jsonObj))
        resource = Resources.objects.get(name=jsonObj["target"])
        resource.disabled = True
        resource.save()
        result_dict = {}
        result_dict["result"] = "success"
        print("[api.views.disabled_resource] end: " + str(datetime.now()))
        return JsonResponse(result_dict)
    return HttpResponse(status=status)


def upload(request):
    status = 200
    if request.FILES:
        print("[api.views.upload] begin: " + str(datetime.now()))
        jsonObj = json.loads(request.POST["json"])[0]
        print("[api.views.upload] jsonObj: " + str(jsonObj))
        print("[api.views.upload] jsonObj['path']: " + jsonObj["path"])
        print("[api.views.upload] jsonObj['target']: " + jsonObj["target"])
        print(
            "[api.views.upload] request.FILES.getlist('file'): "
            + str(request.FILES.getlist("file"))
        )
        task = thread_task(
            request.session._session_key,
            jsonObj["path"],
            jsonObj["target"],
            request.FILES.getlist("file"),
        )
        result_dict = task.upload_files()
        print("[api.views.upload] result_dict: " + str(result_dict))
        print("[api.views.upload] end: " + str(datetime.now()))
        return JsonResponse(result_dict)
    else:
        print("[api.views.upload] no files")
    return HttpResponse(status=status)


def command(request):
    status = 500
    if request.method == "POST":
        print("[api.views.command] begin: " + str(datetime.now()))
        jsonObj = json.loads(request.body)[0]
        print("[api.views.command] jsonObj: " + str(jsonObj))
        # jsonObj["command"] is always single
        resource = Resources.objects.get(name=jsonObj["target"])
        t = target(resource)
        if not t.connect():
            print("[api.views.command] cannot connect to " + jsonObj["target"])
            return HttpResponse(status=status)
        result_dict = {}
        result_dict["message"] = jsonObj["message"]
        result_dict["result"] = t.run(jsonObj["command"])
        t.disconnect()
        print("[api.views.command] result_dict: " + str(result_dict))
        print("[api.views.command] end: " + str(datetime.now()))
        return JsonResponse(result_dict)
    return HttpResponse(status=status)


def reboot(request):
    status = 500
    if request.method == "POST":
        print("[api.views.reboot] begin: " + str(datetime.now()))
        jsonObj = json.loads(request.body)[0]
        print("[api.views.reboot] jsonObj: " + str(jsonObj))
        # jsonObj["reboot"] is always single
        resource = Resources.objects.get(name=jsonObj["target"])
        t = target(resource)
        if not t.connect():
            print("[api.views.reboot] cannot connect to " + jsonObj["target"])
            return HttpResponse(status=status)
        result_dict = {}
        result_dict["message"] = jsonObj["message"]
        result_dict["result"] = t.reboot()
        t.disconnect()
        print("[api.views.reboot] result_dict: " + str(result_dict))
        print("[api.views.reboot] end: " + str(datetime.now()))
        return JsonResponse(result_dict)
    return HttpResponse(status=status)
