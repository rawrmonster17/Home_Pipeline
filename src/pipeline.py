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

    def file_or_folder_sender(self, local_path, remote_path):
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
        while shell.recv_ready():
            output += shell.recv(1024).decode()
        # Remove the command prompt from the output
        output = "\n".join(output.splitlines()[:-1])
        error_output = ""
        while shell.recv_stderr_ready():
            error_output += shell.recv_stderr(1024).decode()
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

    def run_python_script_in_venv(self, script_path, venv_path, requirements_path=None):
        # Make sure venv is installed
        self.run_sudo_command('apt install python3-venv -y')
        # Create the virtual environment
        self.run_sudo_command(f'python3 -m venv {venv_path}')
        # Activate the virtual enviroment
        source_command = f'source {venv_path}/bin/activate'
        # If a requirements file is provided install the requirements
        if requirements_path is not None:
            self.run_sudo_command(f'{source_command} && pip install -r {requirements_path}')
        # Run the script
        result = self.run_sudo_command(f'{source_command} && python3 {script_path}')
        return result


if __name__ == "__main__":
    print("This is a class library file."
          " Please do not run this file directly.")
