'''The function of this library file is to hold all of the code that is
meant to be reused on computers.'''
import json


class Computer:

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def update_apt_repo(self):
        command = "apt-get update"
        return self.ssh_client.run_sudo_command(command)

    def check_apt_upgrades(self):
        command = "apt list --upgradable"
        output_json = self.ssh_client.run_command(command)
        output = json.loads(output_json)["stdout"]
        lines = output.split('\n')[1:]  # Ignore the first line
        packages = []
        for line in lines:
            if line:  # Ignore empty lines
                package = line.split('/')[0]
                version = line.split()[1]
                packages.append(f'{package} {version}')
        return packages

    def check_for_reboot_required(self):
        command = "test -f /var/run/reboot-required && echo true || echo false"
        return self.ssh_client.run_command(command)

    def reboot_if_required(self):
        bool_value = self.check_for_reboot_required()
        if bool_value:
            command = "reboot"
            return self.ssh_client.run_sudo_command(command)
        else:
            pass
