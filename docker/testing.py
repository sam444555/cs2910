import sys, subprocess, time, os
from datetime import datetime

######################################
######################################
#### configurable test parameters ####
######################################
######################################

# total number of updates a trial should send (default 25k) 
total_updates=25000
# total number of replicas used (default 6)
num_replicas=6
# bandwidth limit (default: none, 100/250/500/750 Mbps)
bandwidth_limit =  ['inf',100,250,500,750]
bandwidth_limit =  ['inf']


# create the results file in csv format
# limit,clients,trial#,time_sec,stalls,expected_throughput,actual_throughput,min_latency,max_latency,avg_latency
file_num=0
results_file=f'test_results/results{file_num}.csv'

while os.path.exists(results_file):
    file_num+=1
    results_file=f'test_results/results{file_num}.csv'


# limit (in Mbps) where "inf" = no limit applied
for limit in bandwidth_limit:
    # apply the limit to all 6 replicas
    for replica_id in range(1,num_replicas+1):
        if limit!='inf':
            subprocess.run(
                f"docker exec prime{replica_id} tc qdisc replace dev eth0 root handle 1: htb default 10",
                shell=True,
                check=True
            )

            subprocess.run(
                f"docker exec prime{replica_id} tc class replace dev eth0 parent 1: classid 1:10 htb rate {limit}mbit",
                shell=True,
                check=True
            )
    # test the following number of clients
    for num_emulated_clients in [1,5,10,15,20,25,30,50,100]:
        # 3 trials per client
        for trial_num in range(1,6):
            results = subprocess.run(
            f'docker exec prime1 /root/cs2910/prime/bin/driver -l 172.20.0.2 -i 1 -s 1 -c {total_updates} -n {num_emulated_clients} -LS {0} -trialnum {trial_num}',shell=True,
            capture_output=True,
            text=True 
            )

            time.sleep(5)

            # get the stdout from the driver program and find and parse the line with the results of the trial
            print(results.stdout, flush=True)

            with open(results_file, "a") as f:
                f.write(results.stdout)