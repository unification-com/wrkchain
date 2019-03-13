from compose.config.config import Config
from compose.config.serialize import serialize_config
from compose.config.types import ServicePort

COMPOSE_VERSION = '3.2'
GETH_BASE_PORT = 30305
MAX_EVS = 256

port_list = [GETH_BASE_PORT + x for x in range(MAX_EVS)]
ip_list = [x + 2 for x in range(16)]


def get_ip():
    index = ip_list.pop(0)
    return f'172.25.0.{index}'


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
                'ipv4_address': get_ip()
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

def generate_validators(
        validators, bootnode, bootnode_id, workchain_id, with_rpc=False):
    d = []
    n = 0

    for validator in validators:
        n = n + 1
        geth_port = port_list.pop(0)
        enode = f'enode://{bootnode_id}@{bootnode["ip"]}:{bootnode["port"]}'
        cmd = f'/usr/bin/geth ' \
              f'--bootnodes {enode} ' \
              f'--etherbase {validator["address"]} ' \
              f'--gasprice "0" ' \
              f'--password /root/.walletpassword ' \
              f'--port {geth_port} ' \
              f'--mine ' \
              f'--networkid {workchain_id} ' \
              f'--syncmode=full ' \
              f'--unlock {validator["address"]} ' \
              f'--verbosity=4 '

        if with_rpc:
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

        if with_rpc:
            name = f'workchain-rpc-validator-{n}'
        else:
            name = f'workchain-validator-{n}'

        if with_rpc:
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
                    'ipv4_address': get_ip()
                }
            },
            'build': build_d,
            'command': cmd
        })
    return d


def generate(config, bootnode_address, workchain_id):
    workchain = config['workchain']
    validators = workchain['validators']
    rpc_nodes = workchain['rpc_nodes']
    bootnode_cfg = workchain['bootnode']

    services = []
    if bootnode_cfg['use']:
        services.append(bootnode(bootnode_cfg))

    rpc_nodes = generate_validators(
        rpc_nodes, bootnode_cfg, bootnode_address, workchain_id, with_rpc=True)
    services = services + rpc_nodes

    evs = generate_validators(
        validators, bootnode_cfg, bootnode_address, workchain_id)
    services = services + evs

    if config['workchain']['chaintest'] == True:
        services = services + [chaintest()]

    networks = {'chainnet':
                    {'driver': 'bridge', 'ipam':
                        {'config': [{'subnet': '172.25.0.0/24'}]}}}

    config = Config(version=COMPOSE_VERSION, services=services, volumes=[],
                    networks=networks, secrets=[], configs=[])
    return serialize_config(config, None)
