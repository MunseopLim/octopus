import threading


class command_thread(threading.Thread):
    def __init__(self, result_dict, target, command_str):
        super().__init__()
        self.name = "command_thread_for_" + target.name
        self.result_dict = result_dict
        self.target = target
        self.command_str = command_str
        print("[api.command_thread.__init__] target.name: " + target.name)
        print("[api.command_thread.__init__] command_str: " + command_str)

    def run(self):
        # fail case
        if not self.target.connect():
            self.result_dict[self.target.name] = "Fail"
            return
        # run
        result = self.target.run(self.command_str)
        self.result_dict[self.target.name] = result
        self.target.disconnect()
