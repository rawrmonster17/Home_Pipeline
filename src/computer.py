'''The function of this library file is to hold all of the code that is
meant to be reused on computers.'''
import json
import time


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
        output_json = self.ssh_client.run_command(command)
        command = json.loads(output_json)["stdout"]
        # with out strip it wasn't working
        if str(command).lower().strip() == "true":
            return True
        else:
            return False

    def reboot_if_required(self):
        time_check = self.check_if_ok_to_reboot()
        if time_check:
            bool_value = self.check_for_reboot_required()
            if bool_value:
                command = "reboot"
                return self.ssh_client.run_sudo_command(command)
            else:
                pass
        else:
            print("Not time to reboot yet")
            # I need to create a way to schedule the reboot to happen at 3am
            # if a reboot is required.
            self.ssh_client.schedule_reboot()

    def apt_upgrade(self):
        command = "apt upgrade -y"
        return self.ssh_client.run_sudo_command(command)
    
    def check_if_ok_to_reboot(self):
        # I want to check if it is around 3am - 4am in the morning.
        # if it is I want to return true else false.
        # get current time
        current_time = time.localtime()
        # check if time is between 3am and 4am
        if current_time.tm_hour >= 3 and current_time.tm_hour < 4:
            return True
        else:
            return False
    
    def schedule_reboot(self):
        # If this method is called I want it to reboot the machine at 3am one time.
        reboot_command = "reboot --force 03:00"
        print("Scheduling reboot for 3am")
        return self.ssh_client.run_sudo_command(reboot_command)
        
        
