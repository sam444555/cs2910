import sys, subprocess, time, os

# replica id 
id = int(sys.argv[1])

# replica ip address (ip = 172.20.0.[0 + replica id + 1])
ip = f'172.20.0.{id+1}'


# # One way delay in milliseconds (RTT = delay_ms*2)
# delay_ms = 0
# # Link speed in megabits/sec
# rate_mbps = 100
# subprocess.run(
#     f"tc qdisc add dev eth0 root netem delay {delay_ms}ms rate {rate_mbps}mbit",
#     shell=True,
#     check=True
# )


# start spines: ./spines -I <ip address> 
spines = subprocess.Popen(
    f"./spines -I {ip}",
    cwd='/root/cs2910/prime/spines/daemon',
    shell=True
)

# give spines time to start
time.sleep(5)

# start prime: ./prime -i <server id> -g <global id>
subprocess.Popen(
    f"./prime -i {id} -g {id}",
    cwd='/root/cs2910/prime/bin',
    shell=True
)

# # give prime 30 seconds to start
# time.sleep(30)

# # wait for synchronized driver start
# while not os.path.exists("/sync/go"):
#     time.sleep(0.01)

# # start driver
# subprocess.Popen(
#     f"./driver -l {ip} -i {id} -s {id} -c 4167 -n 25",
#     cwd='/root/cs2910/prime/bin',
#     shell=True
# )

# wait for spines to terminate then terminate 
spines.communicate()