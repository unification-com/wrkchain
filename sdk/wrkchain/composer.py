from compose.config.config import Config
from compose.config.serialize import serialize_config
from compose.config.types import ServicePort

from wrkchain import constants
from wrkchain.architectures.debian import generate_geth_cmd

COMPOSE_VERSION = '3.3'


def bootnode(config):
    name = 'wrkchain_bootnode'
    return {
        'name': name,
        'hostname': name,
        'container_name': name,
        'ports': [ServicePort(
            published=config['docker_port'], target=config['docker_port'],
            protocol='udp', mode=None, external_ip=None),
        ],
        'networks': {
            'wrkchainnet': {
                'ipv4_address': config['docker_ip']
            }
        },
        'build': {
            'context': '..',
            'dockerfile': 'Docker/bootnode/Dockerfile',
            'args': {
                'GO_VERSION': constants.GO_VERSION,
            },
        },
        'environment': [f'BOOTNODE_PORT={config["docker_port"]}'],
        'command': f'/root/.go/bin/bootnode -nodekey '
        f'/root/node_keys/bootnode.key -verbosity 4 --addr :{config["docker_port"]}',
        'expose': [config["docker_port"]]

    }


def chaintest(config):
    name = 'chaintest'
    return {
        'name': name,
        'hostname': name,
        'container_name': name,
        'networks': {
            'wrkchainnet': {
                'ipv4_address': config['ip']
            }
        },
        'build': {
            'context': '..',
            'dockerfile': 'Docker/chaintest/Dockerfile',
            'args': {
                'GO_VERSION': constants.GO_VERSION,
            },
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
            validator, bootnode_config, wrkchain_id,
            validator['docker_listen_port'])

        build_d = {
            'context': '..',
            'dockerfile': 'Docker/node/Dockerfile',
            'args': {
                'WALLET_PASS': 'pass',
                'PRIVATE_KEY': validator['private_key'],
                'GO_VERSION': constants.GO_VERSION,
            },
        }

        ports = []
        expose_ports = []
        if validator['rpc']:
            rpc_port = validator['rpc']['docker_port']
            ports.append(ServicePort(
                published=rpc_port, target=rpc_port, protocol=None,
                mode=None, external_ip=None))
            expose_ports.append(rpc_port)

        if validator['is_validator']:
            geth_listen_port = validator['docker_listen_port']
            ports.append(ServicePort(
                published=geth_listen_port, target=geth_listen_port,
                protocol=None, mode=None, external_ip=None))
            expose_ports.append(geth_listen_port)

        d.append({
            'name': name,
            'hostname': name,
            'container_name': name,
            'ports': ports,
            'networks': {
                'wrkchainnet': {
                    'ipv4_address': validator['docker_ip']
                }
            },
            'build': build_d,
            'command': cmd,
            'expose': expose_ports
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

    if config['wrkchain']['chaintest']['use']:
        services = services + [chaintest(config['wrkchain']['chaintest'])]

    networks = {
        'wrkchainnet': {
            'driver': 'bridge',
            'ipam': {
                'config': [{'subnet': config['docker_network']['subnet']}]
            }
        }
    }

    config = Config(version=COMPOSE_VERSION, services=services, volumes=[],
                    networks=networks, secrets=[], configs=[])
    return serialize_config(config, None)
