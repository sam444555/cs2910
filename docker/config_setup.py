import sys, subprocess, os; from pathlib import Path

# Restore the address.config file to its docker configuration
address_config = '1 172.20.0.2\n2 172.20.0.3\n3 172.20.0.4\n4 172.20.0.5\n5 172.20.0.6\n6 172.20.0.7'
config_path = Path(__file__).resolve().parent.parent / "prime/bin/address.config"

with open(config_path, 'w') as f:
    f.write(address_config)

# Restore the spines_address.config file to its docker configuration
address_config = '1 172.20.0.2\n2 172.20.0.3\n3 172.20.0.4\n4 172.20.0.5\n5 172.20.0.6\n6 172.20.0.7'
config_path = Path(__file__).resolve().parent.parent / "prime/bin/spines_address.config"

with open(config_path, 'w') as f:
    f.write(address_config)

# Restore spines.conf
config_path = Path(__file__).resolve().parent.parent / "prime/spines/daemon"
address_config = """
# List of hosts in the network, Starting with ID = 1
# Format: [ID] [IP_ADDRESS]
Hosts 
{
    # replica 1 [docker]
    1 172.20.0.2
    # replica 2 [docker]
    2 172.20.0.3
    # replica 3 [docker]
    3 172.20.0.4
    # replica 4 [docker]
    4 172.20.0.5
    # replica 5 [docker]
    5 172.20.0.6
    # replica 6 [docker]
    6 172.20.0.7
}
    
# Lists of edges in the network. If Directed_Edges = True 
#       above, specify each edge in both directions.
#       Otherwise, specify each edge only once.
Edges 
{
    # ID1 ID2 COST
        1   2   1
        1   3   1
        1   4   1
        1   5   1
        1   6   1
        2   3   1
        2   4   1
        2   5   1
        2   6   1
        3   4   1
        3   5   1
        3   6   1
        4   5   1
        4   6   1
        5   6   1
}
 """
example = (config_path / "example_spines.conf").read_text()
(config_path / "spines.conf").write_text(example + "\n" + address_config)