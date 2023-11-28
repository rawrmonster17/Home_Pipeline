# The purpose of this is to use the pipeline and one password
# to move my movies and videos to my server.

class Movie:
    
    def __init__(self, ssh_client):
        self.sshClient = ssh_client