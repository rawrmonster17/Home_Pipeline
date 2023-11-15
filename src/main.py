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
    pipelineobj.send_file(file_to_send, remote_path)
    computerobj = computer.Computer(pipelineobj)
    output = computerobj.check_for_reboot_required()
    if output:
        print("Reboot required")
        # I want to add the reboot here but not yet.
        # computerobj.reboot_if_required()
    else:
        pass
    output = computerobj.check_apt_upgrades()
    print(output)
