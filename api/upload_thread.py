import threading


class upload_thread(threading.Thread):
    def __init__(
        self, result_dict, target, local_file_path_list, remote_file_path_list
    ):
        super().__init__()
        self.name = "upload_thread_for_" + target.name
        self.result_dict = result_dict
        self.target = target
        self.local_file_path_list = local_file_path_list
        self.remote_file_path_list = remote_file_path_list
        print("[api.upload_thread.__init__] target: " + str(target))
        print(
            "[api.upload_thread.__init__] local_file_path_list: "
            + str(local_file_path_list)
        )
        print(
            "[api.upload_thread.__init__] remote_file_path_list: "
            + str(remote_file_path_list)
        )

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
        result = self.target.upload(
            self.local_file_path_list, self.remote_file_path_list
        )
        self.result_dict[self.target.name] = result
        self.target.disconnect()
