#!/usr/bin/python3
import subprocess
import re


class OnePasswordManager:
    def __init__(self, vault="Development"):
        self.vault = vault

    def run_op_command(self, command):
        try:
            # Construct the command to run the 1Password CLI
            op_command = ["op", *command, "--vault", self.vault]

            # Run the command and capture the output
            process = subprocess.Popen(op_command,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Check if the command was successful
            if process.returncode == 0:
                return stdout.decode("utf-8")
            else:
                return f"Error: {stderr.decode('utf-8')}"
        except Exception as e:
            return str(e)

    def parse_user_password_website(self, text):
        # Define the regex patterns to search for
        username_pattern = r"username:\s+(\S+)"
        password_pattern = r"password:\s+(\S+)"
        website_pattern = r"website:\s+(\S+)"
        # Search for the patterns in the text
        username_match = re.search(username_pattern, text)
        password_match = re.search(password_pattern, text)
        website_match = re.search(website_pattern, text)
        # Extract the values from the regex search
        username = (
            username_match.group(1) if username_match else "Username not found"
        )
        password = (
            password_match.group(1) if password_match else "Password not found"
        )
        website = (
            website_match.group(1) if website_match else "Website not found"
        )
        # Return the results
        try:
            return {
                "username": username,
                "password": password,
                "website": website
            }
        except Exception as e:
            return str(e)


# Example usage:
if __name__ == "__main__":
    print("This is the start of a class file."
          " It will not be called directly in the future")
