class built_in_test_stage:
    def __init__(self, target, result):
        self.target = target
        self.result = result

    def run_command_get_result(self, command_string):
        return self.target.run(command_string)

    def get_result_of_test_stage(self, test_stage_dict):
        result = self.run_command_get_result(test_stage_dict["test_command"]).strip(
            " \n"
        )
        return self.make_result_message(result, test_stage_dict)

    def add_result_of_built_in_check_connection(self):
        str = "connecting to addresses on the list"
        connect_addr_list = self.target.connect_addr_list.split("/")
        if self.contains_addr(connect_addr_list):
            for connection in connect_addr_list:
                connect_result = self.run_command_get_result(
                    "ping -c 1 " + connection
                ).strip(" \n")
                if "Destination Host Unreachable" in connect_result:
                    self.result[str] = "Fail"
                    return
            self.result[str] = "OK"
        else:
            self.result[str] = "No list"

    def add_result_of_built_in_check_ci_agent(self):
        str = "running ci agent"
        cmd_result = self.run_command_get_result("ps -e|grep wrapper").strip(" \n")
        if cmd_result:
            self.result[str] = "OK"
        else:
            self.result[str] = "Fail"

    def contains_addr(self, addr_list):
        if len(addr_list) == 1 and addr_list[0] == "":
            return False
        else:
            return True

    def run(self):
        self.add_result_of_built_in_check_connection()
        self.add_result_of_built_in_check_ci_agent()
