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
    nodes = config['workchain']['nodes']
    for i in range(len(nodes)):
        if nodes[i]['write_to_oracle'] and nodes[i]['address'] not in \
                oracle_addresses:
            oracle_addresses.append(nodes[i]['address'])

    return oracle_addresses


def check_overrides_in_config(overrides, config):
    for key, data in overrides.items():
        if isinstance(data, dict):
            check_overrides_in_config(data, config[key])
        elif isinstance(data, list):
            for i in range(len(data)):
                ov = data[i]
                co = config[key][i]
                if isinstance(ov, dict):
                    check_overrides_in_config(ov, co)
        else:
            if data == config[key]:
                print(f'{key}: Overridden in config:')
                print(f'Override: {data}')
                print(f'Config: {config[key]}')
            elif key == 'rpc' and isinstance(data, bool):
                print("SKIP RPC BOOL")
            else:
                print(f'{key}: NO MATCH:')
                print(f'Override: {data}')
                print(f'Config: {config[key]}')
