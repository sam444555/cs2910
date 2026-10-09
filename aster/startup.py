import sys, subprocess, time, os, socket

machine_id = int(socket.gethostname().split('.')[0][5:])
print(machine_id)