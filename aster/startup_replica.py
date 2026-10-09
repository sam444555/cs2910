import sys, subprocess, time, os, socket

# get the aster id 
machine_id = int(socket.gethostname().split('.')[0][5:])
print(f'Now running on Aster {machine_id}')

while True:
    # should be in cs2910/aster - run the config to update files accordingly using config_setup.py
    subprocess.run(
    ["python", "config_setup.py","d"],
    text=True
    )
    while True:
        time.sleep(500)
