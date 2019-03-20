from pathlib import Path
from shutil import rmtree

from jinja2 import Environment, FileSystemLoader

from wrkchain.utils import template_root


def generate_directories(build_dir: Path):
    ansible_dir = build_dir / 'ansible'

    if ansible_dir.exists():
        rmtree(str(ansible_dir))

    ansible_dir.mkdir(parents=True)


def generate_ansible(build_dir, config):
    build_root = Path(build_dir)

    loader = FileSystemLoader(str(template_root() / 'ansible'))
    environment = Environment(loader=loader)
    template = environment.get_template('validator.yml')
    context = {
        'validator_name': 'temp'
    }
    built = template.render(context)

    generate_directories(build_root)

    target = build_root / 'ansible' / 'validator.yml'
    target.write_text(built)
