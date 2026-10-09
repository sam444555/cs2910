import sys, subprocess, time, os, socket

# set up spines 
def setup_spines():
    spines_path = "../prime/spines"
    try:

        subprocess.run(["chmod", "+x", "configure"], cwd=spines_path, check=True)
        subprocess.run(["chmod", "+x", "stdutil/configure"], cwd=spines_path, check=True)
        subprocess.run(["chmod", "-R", "+x", "stdutil/buildtools"], cwd=spines_path, check=True)
        subprocess.run(["chmod", "+x", "libspread-util/configure"], cwd=spines_path, check=True)
        subprocess.run(["chmod", "-R", "+x", "libspread-util/buildtools"], cwd=spines_path, check=True)

        print("Configuring Spines...", flush=True)
        subprocess.run(["./configure"], cwd=spines_path, check=True)

        print("Building parser...", flush=True)
        subprocess.run(["make", "-C", "daemon", "parser"], cwd=spines_path, check=True)

        print("Building Spines...", flush=True)
        subprocess.run(["make"], cwd=spines_path, check=True)

        print('Generating Spines keys...', flush=True)
        subprocess.run(
            "chmod +x gen_keys.sh && ./gen_keys.sh",
            cwd=spines_path + "/daemon",
            shell=True,
            check=True
        )

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", flush=True)

    finally:
        print("Spines successfully setup!", flush=True)

# set up prime 
def setup_prime():
    prime_path = "../prime"
    try:
        subprocess.run(
            "chmod +x stdutil/configure && "
            "chmod -R +x stdutil/buildtools && "
            "chmod +x libspread-util/configure && "
            "chmod -R +x libspread-util/buildtools && "
            "chmod +x OpenTC-1.1/TC-lib-1.0/configure && "
            "chmod +x OpenTC-1.1/TC-lib-1.0/missing",
            cwd=prime_path,
            shell=True,
            check=True)

        subprocess.run(["make","clean"], cwd=prime_path+'/src')
        subprocess.run(["make"], cwd=prime_path+'/src')
        
        print('Generating Primes keys...', flush=True)
        subprocess.run(["./gen_keys"], cwd=prime_path+'/bin')

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", flush=True)
        input("Press enter to exit")
        sys.exit(1)

    finally:
        print("Prime successfully setup!", flush=True)

# start spines, prime, and driver (if on replica 13)
def startup():
    print('bye!')


def main():
    # get the aster id 
    machine_id = int(socket.gethostname().split('.')[0][5:])
    print(f'Now running on Aster {machine_id}')

    # should be in cs2910/aster - run the config to update files accordingly using config_setup.py
    subprocess.run(
        ["python", "config_setup.py","d"],
        text=True)

    # update repo and only remake/setup in the event of an update
    result = subprocess.run(
        ["git", "pull"],
        cwd="..",
        capture_output=True,
        text=True,
        check=True
    )



    if "Already up to date." in result.stdout:
        startup()
    else:
        setup_spines()
        print("spines setup!")
        time.sleep(500000)
        setup_prime()

if __name__ == "__main__":
    main()        

