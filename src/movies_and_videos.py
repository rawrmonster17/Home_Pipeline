# The purpose of this is to use the pipeline and one password
# to move my movies and videos to my server.
import json
import os

class Movie:
    
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client
        self.local_movie = "D:\\Torrent\\Movies\\"
    
    def list_of_movie_folders(self):
        list_of_movies = os.listdir(self.local_movie)
        return list_of_movies
    
    def list_remote_movie_folders(self):
        command = "ls /mnt/Storage/Jellyfin/Movies/"
        output_json = self.ssh_client.run_command(command)
        output = json.loads(output_json)["stdout"]
        lines = output.split('\n')[1:]
        new_lines = []
        for line in lines:
            if line:
                line = line.split('/')[0]
                new_lines.append(line)
        return new_lines
    
    def compare_movie_folders(self):
        local_movies = self.list_of_movie_folders()
        remote_movies = self.list_remote_movie_folders()
        for movie in local_movies:
            if movie not in remote_movies:
                self.send_movie_folder(movie)
            else:
                print(f"{0} movie already exists", movie)
    
    def send_movie_folder(self, movie):
        local_path = os.path.join(self.local_movie, movie)
        remote_path = f"/mnt/Storage/Jellyfin/Movies/{movie}"
        print(local_path)
        print(remote_path)
        self.ssh_client.file_or_folder_sender(local_path, remote_path)