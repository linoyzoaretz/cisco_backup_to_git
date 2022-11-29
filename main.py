import time
import tempfile
import os
import subprocess
from netmiko import ConnectHandler

# Cisco IOS-XE connection details
device = {
    "device_type": "cisco_ios",
    "host": "10.1.1.2",
    "username": "cisco",
    "password": "cisco",
}
# Git repository details
git_repo_url = "https://github.com/linoyzoaretz/backup_ios_to_github.git"
commit_message = "Automatic config update"

# ------ Connect to device and get device config ------

# Connect to IOS-XE device
net_connect = ConnectHandler(**device)

# Run show command on device
device_config = net_connect.send_command("show run")

# Disconnect from Device
net_connect.disconnect()

# ------ Clone git repo in temporary directory, replace files with new config file and push changes back to git repo  ------

# Create temporary directory
temporary_folder = "C:/Users/Linoy/AppData/Local/Temp/backups_GIT"
print("temp folder: ", temporary_folder)

print("git clone---------->")
# Clone Git Repo
subprocess.call(f"cd{temporary_folder} && git clone {git_repo_url}", shell=True
                )
# git init (needed?)

print("write file---------->")
# Write all config to file
with open(f"{temporary_folder}/{device['host']}_config_5.txt", "w") as outfile:
    outfile.write(device_config)

print("git add---------->")
subprocess.call(f"cd {temporary_folder} && git add *.txt",
                shell=True,
                )

time.sleep(5)

print("git commit---------->")
subprocess.call(f"cd {temporary_folder} && git commit -o *.txt -m 'commit config file'",
                shell=True,
                )
subprocess.call(f"cd {temporary_folder} && git status",
                shell=True,
                )

# print("git push---------->")
# subprocess.call(f"cd {temporary_folder} && git push -u -f origin master",
#                shell=True,
#                )

# remove file with absolute path
# os.remove("C:/Users/Linoy/AppData/Local/Temp/backups_GIT/*.txt")

# Delete temporary directory
# temporary_folder.cleanup()
