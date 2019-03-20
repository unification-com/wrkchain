from pathlib import Path
from shutil import copytree, rmtree

from jinja2 import Environment, FileSystemLoader

from wrkchain.utils import template_root


def generate_directories(build_dir: Path):
    ansible_dir = build_dir / 'ansible'

    if ansible_dir.exists():
        rmtree(str(ansible_dir))

    ansible_dir.mkdir()
    (ansible_dir / 'roles').mkdir()


def copy_role(build_dir: Path, template_dir: Path, role):
    role_path = template_dir / 'ansible' / 'roles' / role

    ansible_dir = build_dir / 'ansible'
    role_dir = ansible_dir / 'roles' / role

    copytree(str(role_path), str(role_dir))


def generate_ansible(build_dir, config):
    build_root = Path(build_dir)
    templates = template_root()

    loader = FileSystemLoader(str(templates / 'ansible'))
    environment = Environment(loader=loader)
    template = environment.get_template('validator.yml')
    context = {
        'validator_name': 'temp'
    }
    built = template.render(context)

    generate_directories(build_root)
    copy_role(build_root, templates, 'base')

    target = build_root / 'ansible' / 'validator.yml'
    target.write_text(built)
