#!/usr/bin/env python3
import paramiko
import json
import time


class SSHClient:
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.hostname,
                            username=self.username,
                            password=self.password,
                            port=self.port)

    def __del__(self):
        self.client.close()

    def send_file(self, local_path, remote_path):
        sftp = self.client.open_sftp()
        remote_path = remote_path.strip()
        sftp.put(local_path, remote_path)
        sftp.close()

    def run_sudo_command(self, command):
        shell = self.client.invoke_shell()
        shell.send('sudo -S %s\n' % command)
        time.sleep(1)  # Wait for the password prompt
        shell.send('%s\n' % self.password)  # Send the password
        time.sleep(5)  # Allow time for the command to execute
        output = ""
        print("Starting stdout loop")  # Debug print
        while shell.recv_ready():
            output += shell.recv(1024).decode()
        print("Exiting stdout loop")  # Debug print
        # Remove the command prompt from the output
        output = "\n".join(output.splitlines()[:-1])
        error_output = ""
        print("Starting stderr loop")  # Debug print
        while shell.recv_stderr_ready():
            error_output += shell.recv_stderr(1024).decode()
        print("Exiting stderr loop")  # Debug print
        returned_output = {
            "stdout": output,
            "stderr": error_output
        }
        return json.dumps(returned_output)

    def run_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        output = {
            "stdout": stdout.read().decode(),
            "stderr": stderr.read().decode()
        }
        return json.dumps(output)


if __name__ == "__main__":
    print("This is a class library file."
          " Please do not run this file directly.")
