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

def run_tests(sessions):
    # link speed (Mbps) [where 0 is no limit]
    bandwidth = [0,100,250,500,750]
    # total updates sent from the driver program to prime
    total_updates = 25,000
    # number of clients the driver program emulates 
    num_emulated = [1,5,10,15,20,25,30,50,100]
    # number of trials
    num_trials = 5

    results_file = "benchmark_results.txt"
    with open(results_file, "w") as f:
        f.write("Prime Benchmark Results\n\n")

    for speed in bandwidth:
        processes=[]
        if speed>0:
            for i in range(13,19):
                p=subprocess.Popen(
                    f"ssh sjl79@aster{i}.cs.pitt.edu "
                    f"'sudo tc qdisc replace dev eth0 root handle 1: htb default 10 && "
                    f"sudo tc class replace dev eth0 parent 1: classid 1:10 htb rate {speed}mbit'",
                    shell=True)
                processes.append(p)
            for p in processes:p.wait()
        for clients in num_emulated:
            for i in range(1,num_trials+1):
                results = None
                print(f'Running trial {i}, Link Speed {speed}, Num Emulated {clients}')
                # driver only running on replica 13
                subprocess.run(
                    f"ssh sjl79@aster13.cs.pitt.edu "
                    f"'cd ~/cs2910/prime/bin && "
                    f"./driver -l 192.168.53.22 -i 1 -s 1 "
                    f"-c {total_updates} -n {clients} -LS {speed} -trialnum {i}'",
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                with open(results_file, "a") as f:
                    f.write(results.stdout)
                print("Finished!\n")

def main():
    sessions = {}
    id =1
    for i in range(13, 19):
        sessions[i] = subprocess.run(
            f'ssh sjl79@aster{i}.cs.pitt.edu '
            f'"output=$(git -C cs2910 pull 2>&1 || git clone https://github.com/sam444555/cs2910.git 2>&1); '
            f'echo \\"$output\\"; '
            f'cd cs2910/aster && '
            f'python3 -u startup_replica.py {id} \\"$output\\""',
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        id+=1
    next_step = input()
    # stops all the processes on the aster machines and closes all the terminal windows locally
    if next_step=='kill':
        kill_all(sessions)
    elif next_step=='test':
        run_tests(sessions)

if __name__=='__main__':
    main()