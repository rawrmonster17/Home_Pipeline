#!/usr/bin/env python3
import pipeline
import onepasswordcli


if __name__ == '__main__':
    op_manager = onepasswordcli.OnePasswordManager()
    result = op_manager.run_op_command(["item", "get", "server01_ssh"])
    result = op_manager.parse_user_password_website(result)
    file_to_send = "src/test.txt"
    remote_path = "/home/rawrmonster/test.txt"
    pipelineobj = pipeline.SSHClient(result["website"],
                                     result["username"],
                                     result["password"])
    pipelineobj.send_file(file_to_send, remote_path)
