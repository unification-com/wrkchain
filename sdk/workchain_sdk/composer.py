import yaml

COMPOSE_VERSION = '3.2'


def generate():
    # preserve dict ordering when dumping
    yaml.add_representer(
        dict,
        lambda self, data: yaml.representer.SafeRepresenter.represent_dict(
            self, data.items()))

    compose_yaml = dict(
        version=COMPOSE_VERSION
    )
    composition = yaml.dump(compose_yaml)
    return composition
