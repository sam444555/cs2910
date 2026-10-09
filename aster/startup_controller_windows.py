import sys, subprocess, time, os, socket

sessions = {}

for i in range(13, 19):
    sessions[i] = subprocess.Popen(
        f'ssh sjl79@aster{i}.cs.pitt.edu '
        f'"(git -C cs2910 pull || git clone https://github.com/sam444555/cs2910.git) '
        f'&& cd cs2910/aster && python3 startup_replica.py"',
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

