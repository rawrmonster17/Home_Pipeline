'''The function of this library file is to hold all of the code that is
meant to be reused on computers.'''


class Computer:

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def update_apt_repo(self):
        command = "apt-get update"
        return self.ssh_client.run_sudo_command(command)

    def check_apt_upgrades(self):
        command = "apt list --upgradable"
        return self.ssh_client.run_sudo_command(command)

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
