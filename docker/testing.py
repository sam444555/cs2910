import sys, subprocess, time, os

total_updates=50000

# create the results file in csv format
# limit,clients,trial#,time_sec,stalls,expected_throughput,actual_throughput,min_latency,max_latency,avg_latency
file_num=0
results_file=f'test_results/results{file_num}.csv'

while os.path.exists(results_file):
    file_num+=1
    results_file=f'test_results/results{file_num}.csv'

with open(results_file, "w") as f:
    f.write("limit,clients,trial,time_sec,stalls,expected_throughput,actual_throughput,min_latency,max_latency,avg_latency\n")

num_replicas=6
# limit (in Mbps) where "inf" = no limit applied
for limit in ['inf',100,200,300,400,500,600,700,800,900,1000]:
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
    for num_emulated_clients in [10,15,20,25,30,50,75,100,150,200]:
        # 5 trials per client
        for trial_num in range(1,6):
            results = subprocess.run(
            f'docker exec prime1 /root/cs2910/prime/bin/driver -l 172.20.0.2 -i 1 -s 1 -c {total_updates} -n {num_emulated_clients}',shell=True,
            capture_output=True,
            text=True 
            )
            # get the stdout from the driver program and find and parse the line with the results of the trial
            result_line = None
            for line in results.stdout.splitlines():
                if line.startswith("RESULT,"):
                    result_line = line
                    break
            data = result_line.split(',')
            with open(results_file, "a") as f:
                f.write(f"{limit},{num_emulated_clients},{trial_num},{','.join(data[3:])}\n")

    