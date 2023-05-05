import paramiko
from scp import SCPClient


class target:
    def __init__(self, resource) -> None:
        self.ssh = paramiko.SSHClient()
        self.set_env(
            resource.name,
            resource.addr,
            resource.port,
            resource.user_id,
            resource.password,
            resource.connect_addr_list,
            resource.proxy_server,
        )

    def set_env(self, name, ip, port, username, password, connection, proxy_server):
        self.name = name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.connect_addr_list = connection
        self.proxy_server = proxy_server

    def get_env(self):
        return self.name + ", " + self.ip

    def connect(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            proxy = paramiko.ProxyCommand(
                f"ncat --proxy {self.proxy_server.addr}:{self.proxy_server.port} {self.ip} {self.port}"
            )
            self.ssh.connect(
                self.ip,
                port=self.port,
                username=self.username,
                password=self.password,
                sock=proxy,
                timeout=3,
            )
        except Exception as e:
            print(
                "[pages.target.connect] failed to access "
                + self.name
                + "("
                + self.ip
                + ")"
                + ", e: "
                + str(e)
            )
            return False
        print("[pages.target.connect] connect to " + self.name + " successfully")
        return True

    def disconnect(self):
        print("[pages.target.disconnect] disconnect from " + self.name)
        self.ssh.close()

    def run(self, command):
        if self.ssh.get_transport() is not None:
            if not self.ssh.get_transport().is_active():
                return "fail to connect"
            else:
                stdin, stdout, stderr = self.ssh.exec_command(command)
                # return ''.join(stdout.readlines())
                return_string = "".join(stdout.readlines())
                if return_string == "":
                    return_string = "".join(stderr.readlines())
                return return_string
        else:
            return "no transportation"

    def reboot(self):
        if self.ssh.get_transport() is not None:
            if not self.ssh.get_transport().is_active():
                return "fail to connect"
            else:
                stdin, stdout, stderr = self.ssh.exec_command("reboot", timeout=1)
                return "success"
        else:
            return "no transportation"

    def upload(self, local_file_path_list, remote_file_path_list):
        if self.ssh.get_transport() is not None:
            if not self.ssh.get_transport().is_active():
                return "fail to connect"
            else:
                if len(local_file_path_list) != len(remote_file_path_list):
                    print(
                        "[pages.target.upload] target.name: "
                        + self.name
                        + ", len(local_file_path_list) != len(remote_file_path_list)"
                    )
                    return "failed: len(local_file_path_list) != len(remote_file_path_list)"
                try:
                    scp = SCPClient(self.ssh.get_transport())
                    for i in range(len(local_file_path_list)):
                        print(
                            "[pages.target.upload] target.name: "
                            + self.name
                            + ", local_path: "
                            + local_file_path_list[i]
                            + ", remote_path: "
                            + remote_file_path_list[i]
                        )
                        scp.put(
                            local_file_path_list[i],
                            remote_file_path_list[i],
                            preserve_times=True,
                        )
                except Exception as e:
                    return str(e)
                return "success"
        else:
            return "no transportation"

    def check_connectivity(self):
        if self.connect() is True:
            self.disconnect()
            return True
        else:
            self.disconnect()
            return False
