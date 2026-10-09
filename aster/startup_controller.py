import sys, subprocess, time, os, socket

sessions = {}

for i in range(13, 19):
    sessions[i] = subprocess.Popen(
        f'ssh sjl79@aster{i}.cs.pitt.edu "git -C cs2910 pull || git clone https://github.com/sam444555/cs2910.git"',
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

# machine_id = int(socket.gethostname().split('.')[0][5:])
# print(machine_id)