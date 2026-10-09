import sys, subprocess, time, os, socket

# get the aster id 
machine_id = int(socket.gethostname().split('.')[0][5:])
print(f'Now running on Aster {machine_id}')

# should be in cs2910/aster - run the config to update files accordingly using config_setup.py
subprocess.run(
    ["python", "config_setup.py","d"],
    text=True
)

# set up spines 
spines_path = "../prime/spines"
# subprocess.run(["make","clean"], cwd=spines_path, check=True)
try:
    subprocess.run(["./configure"], cwd=spines_path, check=True)
    input("Configure finished. Press Enter to continue...")

    subprocess.run(["make", "-C", "daemon", "parser"], cwd=spines_path, check=True)
    input("Parser finished. Press Enter to continue...")

    subprocess.run(["make"], cwd=spines_path, check=True)
    input("Make finished. Press Enter to continue...")

    subprocess.run(["make", "clean"], cwd=spines_path + "/daemon", check=True)

finally:
    print("Script finished or encountered an error.")
    while True:
        time.sleep(50)