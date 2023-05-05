from django.test import TestCase
from unittest.mock import Mock
from api.command_thread import command_thread
from api.upload_thread import upload_thread


# Create your tests here.
class mock_target(Mock):
    def __init__(self, name, connect_result):
        super().__init__()
        self.name = name
        self.connect_result = connect_result

    def connect(self):
        return self.connect_result

    def run(self, command_str):
        return "Success"

    def disconnect(self):
        return True

    def upload(self, local_file_path_list, remote_file_path_list):
        return "Success"


class test_command_thread(TestCase):
    def test_if_run_successfully(self):
        target_name = "test_target"
        expect_result = "Success"

        mock_t = mock_target(target_name, True)
        command_str = "test_command"
        result_dict = {}
        t = command_thread(result_dict, mock_t, command_str)
        t.start()
        t.join()
        self.assertEqual(result_dict[target_name], expect_result)

    def test_if_connection_failed(self):
        target_name = "test_target"
        expect_result = "Fail"

        mock_t = mock_target(target_name, False)
        command_str = "test_command"
        result_dict = {}
        t = command_thread(result_dict, mock_t, command_str)
        t.start()
        t.join()
        self.assertEqual(result_dict[target_name], expect_result)


class test_upload_thread(TestCase):
    def test_if_run_successfully(self):
        target_name = "test_target"
        expect_result = "Success"

        mock_t = mock_target(target_name, True)
        local_file_path_list = "./test_file"
        remote_file_path_list = "./test/test_file"
        result_dict = {}
        t = upload_thread(
            result_dict, mock_t, local_file_path_list, remote_file_path_list
        )
        t.start()
        t.join()
        self.assertEqual(result_dict[target_name], expect_result)

    def test_if_connection_failed(self):
        target_name = "test_target"
        expect_result = "Fail"

        mock_t = mock_target(target_name, False)
        local_file_path_list = "./test_file"
        remote_file_path_list = "./test/test_file"
        result_dict = {}
        t = upload_thread(
            result_dict, mock_t, local_file_path_list, remote_file_path_list
        )
        t.start()
        t.join()
        self.assertEqual(result_dict[target_name], expect_result)
