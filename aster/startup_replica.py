import sys, subprocess, time, os, socket

# get the aster id 
machine_id = int(socket.gethostname().split('.')[0][5:])
print(f'Now running on Aster {machine_id}')

while True:
    print(os.getcwd())