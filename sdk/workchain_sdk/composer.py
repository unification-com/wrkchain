import yaml

COMPOSE_VERSION = '3.2'


def bootnode():
    name = 'workchain_bootnode'
    return {
        name: {
            'image': 'bootnode',
            'hostname': name,
            'container_name': name,
            'ports': ['30301:30301', '30303:30303']
        }
    }


def generate_validators(n: int):
    d = {}
    for i in range(n):
        name = f'workchain-validator-{i+1}'
        d[name] = {
                'image': 'validator',
                'hostname': name,
                'container_name': name,
            }
    return d


def generate():
    # preserve dict ordering when dumping
    yaml.add_representer(
        dict,
        lambda self, data: yaml.representer.SafeRepresenter.represent_dict(
            self, data.items()))

    compose_yaml = dict(
        version=COMPOSE_VERSION
    )

    evs = generate_validators(3)
    compose_yaml['services'] = dict(
        list(bootnode().items()) + list(evs.items()))

    composition = yaml.dump(compose_yaml)
    return composition
