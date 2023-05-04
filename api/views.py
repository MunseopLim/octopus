from django.http import HttpResponse
from django.http import JsonResponse
from resources.models import Resources
import json
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
from pages.target import target
import threading

class command_thread(threading.Thread):
    def __init__(self, result_dict, target, command_str):
        super().__init__()
        self.name = "command_thread_for_" + target.name
        self.result_dict = result_dict
        self.target = target
        self.command_str = command_str
        print("[api.views.command_thread.__init__] target.name: " + target.name)
        print("[api.views.command_thread.__init__] command_str: " + command_str)

    def run(self):
        # fail case
        if not self.target.connect():
            self.result_dict[self.target.name] = "Fail"
            return
        # run
        result = self.target.run(self.command_str)
        self.result_dict[self.target.name] = result
        self.target.disconnect()


class upload_thread(threading.Thread):
    def __init__(self, result_dict, target, local_file_path_list, remote_file_path_list):
        super().__init__()
        self.name = "upload_thread_for_" + target.name
        self.result_dict = result_dict
        self.target = target
        self.local_file_path_list = local_file_path_list
        self.remote_file_path_list = remote_file_path_list
        print("[api.views.upload_thread.__init__] target: " + str(target))
        print("[api.views.upload_thread.__init__] local_file_path_list: " + str(local_file_path_list))
        print("[api.views.upload_thread.__init__] remote_file_path_list: " + str(remote_file_path_list))

    def run(self):
        # fail case
        if not self.target.connect():
            self.result_dict[self.target.name] = "Fail"
            return
        # build remote path
        # remote_file_path = ()
        # for path in self.local_file_path_list:
        #     remote_file_path.append(self.remote_path + path)
        # run
        result = self.target.upload(self.local_file_path_list, self.remote_file_path_list)
        self.result_dict[self.target.name] = result
        self.target.disconnect()


class MyTask:
    def __init__(self, sig, command_str, server_name_list, files = None):
        print("[api.views.MyTask.__init__] sig: " + sig + ", command_str: " + command_str + ", server_name_list: " + server_name_list)
        self.sig = sig
        self.command_str = command_str
        self.server_name_list = server_name_list
        self.result_dict = {}
        self.resource_list = Resources.objects.filter(disabled=False, name__in=server_name_list.split(','))
        self.files = files

    def command_execute(self):
        print("[api.views.MyTask.command_execute] command_str: " + self.command_str)
        threads = [None] * len(self.resource_list)
        # start all threads
        for i in range(len(self.resource_list)):
            t = target(self.resource_list[i])
            threads[i] = command_thread(self.result_dict, t, self.command_str)
            threads[i].start()
        # wait for all threads
        for i in range(len(threads)):
            threads[i].join()
        print("[api.views.MyTask.command_execute] result: " + str(self.result_dict))
        return self.result_dict

    def upload_files(self):
        print("[api.views.MyTask.upload_files] path: " + self.command_str + ", files: " + str(self.files))
        threads = [None] * len(self.resource_list)
        remote_path_except_file_name = self.command_str
        # store files
        local_file_name_list = []
        remote_file_name_list = []
        for f in self.files:
            print("[api.views.MyTask.upload_files] uploaded file: " + str(f))
            full_path = settings.UPLOAD_FILES_ROOT + "/" + f.name
            fs = FileSystemStorage()
            if fs.exists(full_path):
                print("[api.views.MyTask.upload_files] existed and removed file: " + full_path)
                fs.delete(full_path)
            filename = fs.save(full_path, f)
            local_file_name_list.append(full_path)
            remote_file_name_list.append(self.command_str + "/" + f.name)
            print("[api.views.MyTask.upload_files] stored file: " + str(settings.BASE_DIR) + fs.url(filename))
        # upload files
        # start all threads
        for i in range(len(self.resource_list)):
            t = target(self.resource_list[i])
            threads[i] = upload_thread(self.result_dict, t, local_file_name_list, remote_file_name_list)
            threads[i].start()
        # wait for all threads
        for i in range(len(threads)):
            threads[i].join()
        return self.result_dict


def request(request):
    status = 500
    if request.method == "POST":
        print("[api.views.request] begin: " + str(datetime.now()))
        jsonObj = json.loads(request.body)[0]
        print("[api.views.request] sig: " + request.session._session_key + ", command: " + jsonObj["command"] + ", target: " + jsonObj["target"])
        task = MyTask(request.session._session_key, jsonObj["command"], jsonObj["target"])
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
        jsonObj = json.loads(request.POST['json'])[0]
        print("[api.views.upload] jsonObj: " + str(jsonObj))
        print("[api.views.upload] jsonObj['path']: " + jsonObj["path"])
        print("[api.views.upload] jsonObj['target']: " + jsonObj["target"])
        print("[api.views.upload] request.FILES.getlist('file'): " + str(request.FILES.getlist('file')))
        task = MyTask(request.session._session_key, jsonObj["path"], jsonObj["target"], request.FILES.getlist('file'))
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
