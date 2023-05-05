from django.conf import settings
from django.core.files.storage import FileSystemStorage
from api.command_thread import command_thread
from api.upload_thread import upload_thread
from pages.target import target
from resources.models import Resources
import json


# Create your views here.
class thread_task:
    def __init__(self, sig, command_str, server_name_list, files=None):
        print(
            "[api.thread_task.__init__] sig: "
            + sig
            + ", command_str: "
            + command_str
            + ", server_name_list: "
            + server_name_list
        )
        self.sig = sig
        self.command_str = command_str
        self.server_name_list = server_name_list
        self.result_dict = {}
        self.resource_list = Resources.objects.filter(
            disabled=False, name__in=server_name_list.split(",")
        )
        self.files = files

    def command_execute(self):
        print("[api.thread_task.command_execute] command_str: " + self.command_str)
        threads = [None] * len(self.resource_list)
        # start all threads
        for i in range(len(self.resource_list)):
            t = target(self.resource_list[i])
            threads[i] = command_thread(self.result_dict, t, self.command_str)
            threads[i].start()
        # wait for all threads
        for i in range(len(threads)):
            threads[i].join()
        print("[api.thread_task.command_execute] result: " + str(self.result_dict))
        return self.result_dict

    def upload_files(self):
        print(
            "[api.thread_task.upload_files] path: "
            + self.command_str
            + ", files: "
            + str(self.files)
        )
        threads = [None] * len(self.resource_list)
        remote_path_except_file_name = self.command_str
        # store files
        local_file_name_list = []
        remote_file_name_list = []
        for f in self.files:
            print("[api.thread_task.upload_files] uploaded file: " + str(f))
            full_path = settings.UPLOAD_FILES_ROOT + "/" + f.name
            fs = FileSystemStorage()
            if fs.exists(full_path):
                print(
                    "[api.thread_task.upload_files] existed and removed file: "
                    + full_path
                )
                fs.delete(full_path)
            filename = fs.save(full_path, f)
            local_file_name_list.append(full_path)
            remote_file_name_list.append(self.command_str + "/" + f.name)
            print(
                "[api.thread_task.upload_files] stored file: "
                + str(settings.BASE_DIR)
                + fs.url(filename)
            )
        # upload files
        # start all threads
        for i in range(len(self.resource_list)):
            t = target(self.resource_list[i])
            threads[i] = upload_thread(
                self.result_dict, t, local_file_name_list, remote_file_name_list
            )
            threads[i].start()
        # wait for all threads
        for i in range(len(threads)):
            threads[i].join()
        return self.result_dict
