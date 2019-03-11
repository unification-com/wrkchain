from compose.config.config import Config
from compose.config.serialize import serialize_config
from compose.config.types import ServicePort

COMPOSE_VERSION = '3.2'
GETH_BASE_PORT = 30305


def bootnode(config):
    name = 'workchain_bootnode'
    return {
        'name': name,
        'hostname': name,
        'container_name': name,
        'ports': [ServicePort(
            published=config['port'], target=config['port'], protocol=None,
            mode=None, external_ip=None),
        ],
        'build': {
            'context': '..',
            'dockerfile': 'Docker/bootnode/Dockerfile',
            'args': {
                'BOOTNODE_PORT': config['port'],
            }
        }
    }


def generate_validators(validators, bootnode, bootnode_id, workchain_id):
    d = []
    n = 0

    for validator in validators:
        n = n + 1
        geth_port = GETH_BASE_PORT + n - 1
        enode = f'enode://{bootnode_id}@{bootnode["ip"]}:{bootnode["port"]}'
        cmd = f'/usr/bin/geth ' \
              f'--bootnodes {enode} ' \
              f'--networkid {workchain_id} ' \
              f'--verbosity=4 ' \
              f'--syncmode=full ' \
              f'--mine ' \
              f'--gasprice "0" ' \
              f'--etherbase {validator["address"]} ' \
              f'--unlock {validator["address"]} ' \
              f'--password /root/.walletpassword ' \
              f'--port {geth_port}'
        build_d = {
            'context': '..',
            'dockerfile': 'Docker/validator/Dockerfile',
            'args': {
                'WALLET_PASS': 'pass',
                'PRIVATE_KEY': validator['private_key'],
                'GENESIS_JSON_FILENAME': 'genesis.json',
                'GETH_LISTEN_PORT': GETH_BASE_PORT,
            },
        }

        name = f'workchain-validator-{n}'
        d.append({
            'name': name,
            'hostname': name,
            'container_name': name,
            'build': build_d,
            'command': cmd
        })
    return d


def generate(config, bootnode_address, workchain_id):
    workchain = config['workchain']
    validators = workchain['validators']
    bootnode_cfg = workchain['bootnode']

    services = []
    if bootnode_cfg['use']:
        services.append(bootnode(bootnode_cfg))

    evs = generate_validators(
        validators, bootnode_cfg, bootnode_address, workchain_id)
    services = services + evs

    config = Config(version=COMPOSE_VERSION, services=services, volumes=[],
                    networks=[], secrets=[], configs=[])
    return serialize_config(config, None)
