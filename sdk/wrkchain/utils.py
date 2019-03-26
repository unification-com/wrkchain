import os

from pathlib import Path


def repo_root() -> Path:
    current_script = Path(os.path.abspath(__file__))
    return current_script.parent.parent.parent


def template_root() -> Path:
    return repo_root() / 'templates'


def write_build_file(file_path, file_contents):
    genesis_file = open(file_path, "w")
    genesis_file.write(file_contents)
    genesis_file.close()


def get_oracle_addresses(config):
    oracle_addresses = []
    nodes = config['wrkchain']['nodes']
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


def chmod_tree(path):
    chmod_path = Path(os.path.abspath(path))
    chmod_path.chmod(0o777)
    with os.scandir(chmod_path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file():
                chmod_file = chmod_path / entry.name
                chmod_file.chmod(0o666)
            else:
                sub_dir = chmod_path / entry.name
                chmod_tree(sub_dir)


def dir_tree(directory, max_depth=1):
    if isinstance(directory, str):
        directory = Path(directory)
    tree = f'+ {directory}\n'
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        if depth <=  max_depth:
            spacer = '  ' * depth
            if path.is_file():
                tree += f'{spacer}- {path.name}\n'
            else:
                tree += f'{spacer}+ {path.name}\n'
    return tree
