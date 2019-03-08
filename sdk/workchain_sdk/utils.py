import os

from pathlib import Path


def repo_root() -> Path:
    current_script = Path(os.path.abspath(__file__))
    return current_script.parent.parent.parent


def write_build_file(file_path, file_contents):
    genesis_file = open(file_path, "w")
    genesis_file.write(file_contents)
    genesis_file.close()
    os.chmod(file_path, 0o666)


def get_oracle_addresses(config):
    oracle_addresses = []
    validators = config['workchain']['validators']
    rpc_nodes = config['workchain']['rpc_nodes']
    for i in range(len(validators)):
        if validators[i]['write_to_oracle'] and validators[i]['address'] not in oracle_addresses:
            oracle_addresses.append(validators[i]['address'])

    for i in range(len(rpc_nodes)):
        if rpc_nodes[i]['write_to_oracle'] and rpc_nodes[i]['address'] not in oracle_addresses:
            oracle_addresses.append(rpc_nodes[i]['address'])

    return oracle_addresses
