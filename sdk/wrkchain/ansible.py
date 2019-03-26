from pathlib import Path
from shutil import copy, rmtree

from jinja2 import DebugUndefined, Environment, FileSystemLoader

from wrkchain.utils import template_root


class Validators:
    def __init__(self, context):
        self.context = context

    def write(self, environment, target, relative):
        template = environment.get_template(str(relative))
        for index, validator in enumerate(self.context):
            base, ext = str(relative).split('.')
            dest = target / f'{base}-{index + 1}.{ext}'
            dest.write_text(template.render(validator))


class Bootnode:
    def __init__(self, context):
        self.context = context

    def write(self, environment, target, relative):
        if self.context['use']:
            template = environment.get_template(str(relative))
            dest = target / str(relative)
            dest.write_text(template.render(self.context))


def template_map(source: Path, target: Path, maps: dict):
    loader = FileSystemLoader(str(source))
    environment = Environment(loader=loader, undefined=DebugUndefined)

    for path in [x for x in source.rglob('*') if not x.is_dir()]:
        relative = path.relative_to(source)
        context = maps.get(str(relative))
        dest = target / relative
        if not dest.parent.exists():
            dest.parent.mkdir(parents=True)

        if context:
            if isinstance(context, Validators) or isinstance(context, Bootnode):
                context.write(environment, target, relative)
            else:
                template = environment.get_template(str(relative))
                dest.write_text(template.render(context))
        else:
            copy(str(path), str(dest))


def generate_ansible(build_dir, config):
    build_root = Path(build_dir)
    ansible_dir = build_root / 'ansible'

    workchain_cfg = config['wrkchain']
    bootnode_cfg = workchain_cfg['bootnode']

    validator_builder = Validators(workchain_cfg['nodes'])

    d = {
        'wrkchain-bootnode.yml': Bootnode(bootnode_cfg),
        'wrkchain-node.yml': validator_builder,
        'Vagrantfile': workchain_cfg
    }

    template_map(template_root() / 'ansible', ansible_dir, d)
