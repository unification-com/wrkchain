from compose.config.config import Config
from compose.config.serialize import serialize_config
from compose.config.types import ServicePort

from wrkchain.architectures.debian import generate_geth_cmd

COMPOSE_VERSION = '3.3'


def bootnode(config):
    name = 'wrkchain_bootnode'
    return {
        'name': name,
        'hostname': name,
        'container_name': name,
        'ports': [ServicePort(
            published=config['port'], target=config['port'], protocol='udp',
            mode=None, external_ip=None),
        ],
        'networks': {
            'chainnet': {
                'ipv4_address': config['ip']
            }
        },
        'build': {
            'context': '..',
            'dockerfile': 'Docker/bootnode/Dockerfile'
        },
        'environment': [f'BOOTNODE_PORT={config["port"]}'],
        'command': f'/root/.go/bin/bootnode -nodekey '
        f'/root/node_keys/bootnode.key -verbosity 4 --addr :{config["port"]}'

    }


def chaintest(config):
    name = 'chaintest'
    return {
        'name': name,
        'hostname': name,
        'container_name': name,
        'networks': {
            'chainnet': {
                'ipv4_address': config['ip']
            }
        },
        'build': {
            'context': '..',
            'dockerfile': 'Docker/chaintest/Dockerfile',
        }
    }


def generate_nodes(nodes, bootnode_config, wrkchain_id):
    d = []
    n = 0

    for validator in nodes:
        n = n + 1
        name_list = ['wrkchain']
        if validator['rpc']:
            name_list.append('rpc')

        if validator['is_validator']:
            name_list.append('validator')

        name_list.append(str(n))
        name = '-'.join(name_list)

        cmd = generate_geth_cmd(
            validator, bootnode_config, wrkchain_id, validator['listen_port'])

        build_d = {
            'context': '..',
            'dockerfile': 'Docker/validator/Dockerfile',
            'args': {
                'WALLET_PASS': 'pass',
                'PRIVATE_KEY': validator['private_key'],
                'GETH_LISTEN_PORT': validator['listen_port'],
            },
        }

        ports = []
        if validator['rpc']:
            rpc_port = validator['rpc']['port']
            ports.append(ServicePort(
                published=rpc_port, target=rpc_port, protocol=None,
                mode=None, external_ip=None))

        if validator['is_validator']:
            geth_listen_port = validator['listen_port']
            ports.append(ServicePort(
                published=geth_listen_port, target=geth_listen_port,
                protocol=None, mode=None, external_ip=None))

        d.append({
            'name': name,
            'hostname': name,
            'container_name': name,
            'ports': ports,
            'networks': {
                'chainnet': {
                    'ipv4_address': validator['ip']
                }
            },
            'build': build_d,
            'command': cmd
        })
    return d


def generate(config, bootnode_config, wrkchain_id):
    wrkchain = config['wrkchain']

    services = []
    if bootnode_config['type'] == 'dedicated':
        services.append(bootnode(bootnode_config['nodes']))

    nodes = generate_nodes(
        wrkchain['nodes'], bootnode_config, wrkchain_id)
    services = services + nodes

    if config['wrkchain']['chaintest']:
        services = services + [chaintest(config['wrkchain']['chaintest'])]

    networks = {
        'chainnet': {
            'driver': 'bridge', 'ipam': {
                'config': [{'subnet': '172.25.0.0/24'}]}}}

    config = Config(version=COMPOSE_VERSION, services=services, volumes=[],
                    networks=networks, secrets=[], configs=[])
    return serialize_config(config, None)
