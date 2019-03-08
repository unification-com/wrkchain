from compose.config.config import Config
from compose.config.serialize import serialize_config
from compose.config.types import ServicePort

COMPOSE_VERSION = '3.2'


def bootnode():
    name = 'workchain_bootnode'
    return {
        'name': name,
        'image': 'bootnode',
        'hostname': name,
        'container_name': name,
        'ports': [ServicePort(
            published=30301, target=30301, protocol=None,
            mode=None, external_ip=None),
            ServicePort(
                published=30303, target=30303, protocol=None,
                mode=None, external_ip=None)
        ]
    }


def generate_validators(validators):
    d = []
    n = 1
    for validator in validators:
        n = n + 1
        build_d = {
            'context': '..',
            'dockerfile': 'Docker/validator/Dockerfile',
            'args': {
                'WALLET_PASS': 'pass',
                'PRIVATE_KEY': validator['private_key'],
                'GENESIS_JSON_FILENAME': 'genesis.json'
            }
        }

        name = f'workchain-validator-{n}'
        d.append({
            'name': name,
            'image': 'validator',
            'hostname': name,
            'container_name': name,
            'build': build_d
        })
    return d


def generate(config):
    workchain = config['workchain']
    validators = workchain['validators']

    services = []
    if workchain['bootnode']['use']:
        services.append(bootnode())

    evs = generate_validators(validators)
    services = services + evs

    config = Config(version=COMPOSE_VERSION, services=services, volumes=[],
                    networks=[], secrets=[], configs=[])
    return serialize_config(config, None)
