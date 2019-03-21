from pathlib import Path
from shutil import copy, rmtree

from jinja2 import Environment, FileSystemLoader

from wrkchain.utils import template_root


class Validators:
    def __init__(self, context):
        self.context = context

    def write(self, environment, target, relative):
        template = environment.get_template(str(relative))
        for index, validator in enumerate(self.context['validators']):
            base, ext = str(relative).split('.')
            dest = target / f'{base}-{index + 1}.{ext}'
            dest.write_text(template.render(validator))


def template_map(source: Path, target: Path, maps: dict):
    loader = FileSystemLoader(str(source))
    environment = Environment(loader=loader)

    for path in [x for x in source.rglob('*') if not x.is_dir()]:
        relative = path.relative_to(source)
        context = maps.get(str(relative))
        dest = target / relative
        if not dest.parent.exists():
            dest.parent.mkdir(parents=True)

        if context:
            if isinstance(context, Validators):
                context.write(environment, target, relative)
            else:
                template = environment.get_template(str(relative))
                dest.write_text(template.render(context))
        else:
            copy(str(path), str(dest))


def generate_ansible(build_dir, config):
    build_root = Path(build_dir)
    ansible_dir = build_root / 'ansible'

    provisioner = {
        'home': 'vagrant',
    }

    validators = {
        'validators':
            [
                {
                    'home': 'vagrant',
                    'validator_name': 'validator-1'
                },
                {
                    'home': 'vagrant',
                    'validator_name': 'validator-2'
                }
            ]
    }

    validator_builder = Validators(validators)

    d = {
        'validator.yml': validator_builder,
        'Vagrantfile': validators,
        'roles/geth/tasks/main.yml': provisioner,
    }
    template_map(template_root() / 'ansible', ansible_dir, d)
