import sys, subprocess, time, os, socket

machine_id = int(socket.gethostname().split('.')[0][5:])
print(machine_id)

while True:
    time.sleep(1)