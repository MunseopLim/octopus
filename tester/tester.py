from pages.target import target
from tester.models import TestStage
from django.forms.models import model_to_dict
from tester.built_in_test_stage import built_in_test_stage
import threading

RESULT_OPTION = (
    ("None", "None"),
    ("HTTP", "HTTP"),
    ("HTTPS", "HTTPS"),
    ("SOCKS4", "SOCKS4"),
    ("SOCKS5", "SOCKS5"),
)


class test_thread(threading.Thread):
    def __init__(self, result_dict, target, test_stage_queryset):
        super().__init__()
        self.name = "test_for_" + target.name
        self.result_dict = result_dict
        self.target = target
        self.test_stage_queryset = test_stage_queryset

    def run_command_get_result(self, command_string):
        return self.target.run(command_string)

    def make_result_message(self, result, test_stage_dict):
        str_ok = "display_ok_type"
        str_fail = "display_fail_type"
        if test_stage_dict[str_ok] == "TYPE1":
            if result:
                return "OK"
        elif test_stage_dict[str_ok] == "TYPE3":
            return result

        if test_stage_dict["expect_result"] == result:
            if test_stage_dict[str_ok] == "TYPE2":
                return "OK"
            elif test_stage_dict[str_ok] == "TYPE4":
                return ""

        # fail cases
        if test_stage_dict[str_fail] == "TYPE1":
            return "Fail"
        elif test_stage_dict[str_fail] == "TYPE2":
            return "Fail"
        # elif test_stage_dict[str_fail] == "TYPE3":
        return "None"

    def get_result_of_test_stage(self, test_stage_dict):
        result = self.run_command_get_result(test_stage_dict["test_command"]).strip(
            " \n"
        )
        return self.make_result_message(result, test_stage_dict)

    def run(self):
        str = "connectivity"
        result = {}
        if self.target.connect():
            result[str] = "OK"
        else:
            result[str] = "Fail"
            self.result_dict[self.target.name] = result
            return
        for entry in self.test_stage_queryset:
            single_test_stage = model_to_dict(entry)
            result[single_test_stage["name"]] = self.get_result_of_test_stage(
                single_test_stage
            )

        built_in = built_in_test_stage(self.target, result)
        built_in.run()

        self.result_dict[self.target.name] = result
        self.target.disconnect()


class tester:
    def __init__(self, resource_list) -> None:
        self.resource_list = resource_list
        self.targets = list()
        for entry in resource_list:
            t = target(entry)
            self.targets.append(t)

    def get_test_stage_object_from_db(self):
        return TestStage.objects.filter(disabled=False)

    def run(self):
        test_stage_queryset = self.get_test_stage_object_from_db()
        result_dict = {}
        threads = [None] * len(self.targets)
        # start all threads
        for i in range(len(threads)):
            threads[i] = test_thread(result_dict, self.targets[i], test_stage_queryset)
            threads[i].start()
        # wait for all threads
        for i in range(len(threads)):
            threads[i].join()
        return result_dict
