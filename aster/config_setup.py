import sys, subprocess, os; from pathlib import Path
default_mode = 0


def setup_config(machines,network):
    ips=None
    # use default config (machines 13-18, network 1)
    if machines is None:
        ips = [f'192.168.53.{i+9}' for i in range(13, 19)]
    else:
        base_addr=f'192.168.{network}.{{}}'
        ips=[base_addr.format(m+9) for m in machines]          

    ip_list ={}       
    for i in range(1,21):
        ip_list[f'192.168.53.{i+9}']=i
        ip_list[f'192.168.54.{i+9}']=i
    print('The following machines have been selected for configuration:\n')
    print(f'Using Network # {network}')
    for ip in ips:
        print(f'aster {ip_list[ip]}: {ip}')
    while True and default_mode==0:
        ans = input('Is this selection valid? (1 for yes 0 for no)\n')
        if(ans=='1'):break
        if(ans=='0'):return 0
        print(f'{ans} is an invalid choice, try again.')
    print('\n')


    # set up address.config/spines_address.config (prime)
    address_config = ""
    for id, ip in enumerate(ips, start=1):
        address_config+= f'{id} {ip}\n'
    # write to address.config
    config_path = Path(__file__).resolve().parent.parent / "prime/bin/address.config"
    with open(config_path, 'w') as f:
        f.write(address_config)
    # write to spines_address.config
    config_path = Path(__file__).resolve().parent.parent / "prime/bin/spines_address.config"
    with open(config_path, 'w') as f:
        f.write(address_config)

    # set up spines.config (spines)
    config_path = Path(__file__).resolve().parent.parent / "prime/bin/spines_address.config"

    if network=='53' or network==None:
        network=1
    elif network=='54':
        network=2
    

    address_config = """\n
    # List of hosts in the network, Starting with ID = 1
    # Format: [ID] [IP_ADDRESS]
    Hosts
    {\n"""

    for id, ip in enumerate(ips, start=1):
        address_config+=f'\t\t\t# replica {id} [aster machine #{ip_list[ip]} network {network}]\n'
        address_config+= f'\t\t\t{id} {ip}\n'

    address_config+="""\t\t}\n\n
    # Lists of edges in the network. If Directed_Edges = True 
    # above, specify each edge in both directions.
    # Otherwise, specify each edge only once.
    Edges 
    {
    \t# ID1 ID2 COST\n"""
    for id1 in range(1,len(ips)+1):
        for id2 in range(id1+1,len(ips)+1):
            address_config+=f'\t\t\t{id1} {id2} 1\n'
    address_config+='\t\t}\n'

    config_path = Path(__file__).resolve().parent.parent / "prime/spines/daemon"
    example = (config_path / "example_spines.conf").read_text()
    (config_path / "spines.conf").write_text(example + "\n" + address_config)

    return 1



def main():
    # any arguments passed will automatically trigger default mode
    if len(sys.argv) > 1:
        global default_mode
        default_mode=1
        res = setup_config(None,None)
        if(res):
            print('Configuration files have been set up successfully!\n')
        else:
            print('Something went wrong setting up the configuration files...\n')
        exit(1)

    #ip addresses
    network = None
    # Build the configuration
    while True:
        # Get which local net you are using (https://github.com/sam444555/cs2910/blob/main/aster) as described in the Aster Server Network Configuration Table
        network = input('\nLocal Network 1 or Local Network 2 (enter 1 or 2, or 3 for default settings):\n')
        default=False 
        if network not in ['1','2','3']:
            print(f'Invalid input: {network}, try again.')
            continue
        else:
            if network=='1':
                print('Using Local Network 1')
                network = '53'
            elif network=='2':
                print('Using Local Network 2')
                network = '54'
            else:
                print('Using Default Configuration')
                res = setup_config(None,None)
                if res: break
                else: continue
        # pick machines from 1-20
        machines_choice = input('\nSelect the machines you want to use in a comma separated list in ascending order. \nEx 1,2,3 = aster machines 1 2 and 3\n')
        prev = -1
        aster_list=[]
        for machine in (machines_choice.split(",")):
            machine_int=None
            try:
                machine_int=int(machine)
            except ValueError:
                print(f"Invalid value {machine_int}, must be an integer in range 1-20")
                continue
            if machine_int < prev:
                print(f"{machine_int} is less than {prev}, the machines must be entered in ascending value")
                continue
            if machine_int<1 or machine_int>20:
                print(f"Invalid aster machine id {machine}, it must fall in range 1-20")
                continue
            prev=machine_int
            # valid machine picked, begin constructing the config info
            aster_list.append(machine_int)
        setup_config(aster_list,network)
        print('Config files have successfully been set up!')
        return aster_list
        
if __name__ == "__main__":
    main()        
