# This is a way to automate the process of setting up a new server.
# It uses a combination of the OnePassword CLI and SSH to automate the process of setting up a new server. 
# It is a work in progress and is not ready for production use.
import os

class Setup:

    def __init__(self) -> None:
        self.computerName = os.environ.get("COMPUTER_NAME")
        self.password = os.environ.get("PASSWORD")
        self.username = os.environ.get("USERNAME")
        self.sshKey = os.environ.get("SSH_KEY")