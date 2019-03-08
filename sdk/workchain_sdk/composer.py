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


def generate_validators(n: int):
    d = []
    for i in range(n):
        name = f'workchain-validator-{i+1}'
        d.append({
                'name': name,
                'image': 'validator',
                'hostname': name,
                'container_name': name,
            })
    return d


def generate(config):
    validators = config['workchain']['validators']

    services = []
    if config['workchain']['bootnode']['use']:
        services.append(bootnode())

    evs = generate_validators(len(validators))
    services = services + evs

    config = Config(version=COMPOSE_VERSION, services=services, volumes=[],
                    networks=[], secrets=[], configs=[])
    return serialize_config(config, None)
