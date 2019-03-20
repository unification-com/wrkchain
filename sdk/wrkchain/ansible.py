from pathlib import Path
from shutil import copy, rmtree

from jinja2 import Environment, FileSystemLoader

from wrkchain.utils import template_root


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
            template = environment.get_template(str(relative))
            dest.write_text(template.render(context))
        else:
            copy(str(path), str(dest))


def generate_ansible(build_dir, config):
    build_root = Path(build_dir)
    ansible_dir = build_root / 'ansible'

    validator_one = {
        'home': 'ec2-user',
        'validator_name': 'validator-1'
    }

    d = {
        'validator.yml': validator_one,
        'roles/geth/tasks/main.yml': validator_one,
    }
    template_map(template_root() / 'ansible', ansible_dir, d)
