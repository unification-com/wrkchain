from compose.config.config import Config
from compose.config.serialize import serialize_config
from compose.config.types import ServicePort

COMPOSE_VERSION = '3.3'
GETH_BASE_PORT = 30305
MAX_EVS = 256

port_list = [GETH_BASE_PORT + x for x in range(MAX_EVS)]


def bootnode(config):
    name = 'workchain_bootnode'
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
            'dockerfile': 'Docker/bootnode/Dockerfile',
            'args': {
                'BOOTNODE_PORT': config['port'],
            }
        }
    }


def chaintest():
    name = 'chaintest'
    return {
        'name': name,
        'hostname': name,
        'container_name': name,
        'networks': {
            'chainnet': {
                'ipv4_address': get_ip()
            }
        },
        'build': {
            'context': '..',
            'dockerfile': 'Docker/chaintest/Dockerfile',
        }
    }


def generate_nodes(nodes, bootnode_config, workchain_id):
    d = []
    n = 0

    b_node = bootnode_config['nodes']

    for validator in nodes:
        n = n + 1
        if validator['rpc']:
            name = f'workchain-rpc-validator-{n}'
        else:
            name = f'workchain-validator-{n}'

        geth_port = port_list.pop(0)

        cmd = f'/usr/bin/geth ' \
              f'--etherbase {validator["address"]} ' \
              f'--gasprice "0" ' \
              f'--password /root/.walletpassword ' \
              f'--port {geth_port} ' \
              f'--mine ' \
              f'--networkid {workchain_id} ' \
              f'--syncmode=full ' \
              f'--unlock {validator["address"]} ' \
              f'--verbosity=4 '

        if bootnode_config['type'] == 'dedicated':
            enode = f'enode://{b_node["address"]}@{b_node["ip"]}:' \
                    f'{b_node["port"]}'
            cmd = cmd + f'--bootnodes {enode} '
        else:
            cmd = cmd + f'--nodekey="/root/node_keys/' \
                        f'{validator["address"]}.key" '

        if validator['rpc']:
            cmd = cmd + \
                  f'--rpcport 8101 ' \
                  f'--rpc ' \
                  f'--rpcaddr "0.0.0.0" ' \
                  f'--rpcapi "eth,web3,net,admin,debug,db,personal,miner" ' \
                  f'--rpccorsdomain "*" ' \
                  f'--rpcvhosts "*" '

        build_d = {
            'context': '..',
            'dockerfile': 'Docker/validator/Dockerfile',
            'args': {
                'WALLET_PASS': 'pass',
                'PRIVATE_KEY': validator['private_key'],
                'GETH_LISTEN_PORT': geth_port,
            },
        }

        if validator['rpc']:
            ports = [ServicePort(
                published=8101, target=8101, protocol=None,
                mode=None, external_ip=None),
            ]
        else:
            ports = []

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


def generate(config, bootnode_config, workchain_id):
    workchain = config['workchain']

    services = []
    if bootnode_config['type'] == 'dedicated':
        services.append(bootnode(bootnode_config['nodes']))

    nodes = generate_nodes(
        workchain['nodes'], bootnode_config, workchain_id)
    services = services + nodes

    if config['workchain']['chaintest']:
        services = services + [chaintest()]

    networks = {
        'chainnet': {
            'driver': 'bridge', 'ipam': {
                'config': [{'subnet': '172.25.0.0/24'}]}}}

    config = Config(version=COMPOSE_VERSION, services=services, volumes=[],
                    networks=networks, secrets=[], configs=[])
    return serialize_config(config, None)
