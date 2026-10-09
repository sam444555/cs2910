import sys, subprocess, time, os, socket

def kill_all(sessions):
    for i, process in sessions.items():
        subprocess.run(
            ["ssh", f"sjl79@aster{i}.cs.pitt.edu",
             "pkill -f '[s]tartup_replica.py'"],
            check=False
        )

        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    sessions.clear()

sessions = {}

for i in range(13, 19):
    sessions[i] = subprocess.Popen(
        f'ssh sjl79@aster{i}.cs.pitt.edu '
        f'"(git -C cs2910 pull || git clone https://github.com/sam444555/cs2910.git) '
        f'&& cd cs2910/aster && python3 -u startup_replica.py"',
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

if input()=='kill':
    kill_all(sessions)