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
try:
    print("Configuring Spines...", flush=True)
    subprocess.run(["./configure"], cwd=spines_path, check=True)

    print("Building parser...", flush=True)
    subprocess.run(["make", "-C", "daemon", "parser"], cwd=spines_path, check=True)

    print("Building Spines...", flush=True)
    subprocess.run(["make"], cwd=spines_path, check=True)

    print("All commands completed successfully!", flush=True)

except subprocess.CalledProcessError as e:
    print(f"Command failed: {e.cmd}", flush=True)
    print(f"Exit code: {e.returncode}", flush=True)

finally:
    print("Press Ctrl+C to exit.", flush=True)
    while True:
        time.sleep(50)