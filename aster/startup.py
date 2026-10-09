import sys, subprocess, time, os, socket

if len(sys.argv)<2:
    print('Usage: python startup.py <aster_num>')
    sys.exit(1)

# get the aster num
aster_num = sys.argv[1]


# start an aster machine
ssh = subprocess.Popen(
    f"ssh sjl79@aster13.cs.pitt.edu",
    shell=True
)

# machine_id = int(socket.gethostname().split('.')[0][5:])
# print(machine_id)