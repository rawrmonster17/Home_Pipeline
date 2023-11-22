#!/usr/bin/env python3
import pipeline
import onepasswordcli
import computer


if __name__ == '__main__':
    op_manager = onepasswordcli.OnePasswordManager()
    result = op_manager.run_op_command(["item", "get", "server01_ssh"])
    result = op_manager.parse_user_password_website(result)
    # This will end up being a docker-compose.yml file
    file_to_send = "src/test.txt"
    remote_path = "/home/rawrmonster/test.txt"
    pipelineobj = pipeline.SSHClient(result["website"],
                                     result["username"],
                                     result["password"])
    pipelineobj.file_or_folder_sender(file_to_send, remote_path)
    computerobj = computer.Computer(pipelineobj)
    output = computerobj.check_for_reboot_required()
    if output:
        print("Reboot required")
        computerobj.update_apt_repo()
        computerobj.apt_upgrade()
        computerobj.reboot_if_required()
    else:
        output = computerobj.check_apt_upgrades()
        computerobj.update_apt_repo()
        computerobj.reboot_if_required()
        print("No reboot required and installed updates")
