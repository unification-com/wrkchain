from os import path, symlink, unlink
from pathlib import Path
from shutil import copy

from jinja2 import DebugUndefined, Environment, FileSystemLoader

from wrkchain.utils import template_root


class Validators:
    def __init__(self, context, custom_roles):
        self.context = context
        self.custom_roles = custom_roles

    def role_name(self, name, key):
        return f"{name}_{key}"

    def write(self, environment, target, relative):
        template = environment.get_template(str(relative))
        for index, validator in enumerate(self.context):
            base, ext = str(relative).split('.')
            dest = target / f'{base}-{index + 1}.{ext}'

            eff = {
                'roles': [self.role_name(x, validator['name']) for x in
                          self.custom_roles],
                'validator': validator
            }
            dest.write_text(template.render(eff))

    def link_genesis(self, build_root):
        src = build_root / 'genesis.json'
        dst = build_root / 'ansible/roles/node/files/genesis.json'
        if dst.exists():
            unlink(dst)
        symlink(src, dst)


class Bootnode:
    def __init__(self, context):
        self.context = context

    def write(self, environment, target, relative):
        if self.context['use']:
            template = environment.get_template(str(relative))
            dest = target / str(relative)
            dest.write_text(template.render(self.context))

    def link_bootnode_key(self, build_root):
        build_root_full_path = Path(path.abspath(build_root))
        if self.context['use']:
            src_dir = build_root_full_path / 'node_keys'
            dst_dir = build_root_full_path / 'ansible/roles/bootnode/files/'
            rel_src_dir = Path(path.relpath(src_dir, dst_dir))
            dst = dst_dir / 'bootnode.key'
            src = rel_src_dir / 'bootnode.key'

            if dst.exists():
                unlink(dst)
            symlink(src, dst)


def template_map(source: Path, target: Path, maps: dict):
    loader = FileSystemLoader(str(source))
    environment = Environment(loader=loader, undefined=DebugUndefined)

    for path in [x for x in source.rglob('*') if not x.is_dir()]:
        relative = path.relative_to(source)
        if str(relative).startswith('custom_role'):
            continue

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


def transform_to_node_map(workchain_cfg):
    ret = {}
    for node in workchain_cfg['nodes']:
        ret[node['name']] = node
    return ret


def process_custom_roles(template_root, ansible_dir, node_map):
    source = template_root / 'ansible' / 'custom_roles'

    for path in [x for x in source.glob('*') if x.is_dir()]:
        role_name = path.name

        for node, node_d in node_map.items():
            d = {
                'files/motd': node_d
            }
            apply_custom_role(source, ansible_dir, role_name, node, d)


def apply_custom_role(
        source: Path, target: Path, role_name: str, node_key: str, d: dict):
    target_name = f"{role_name}_{node_key}"
    dest = target / 'roles' / target_name

    custom_role_dir = source / role_name

    if not dest.exists():
        dest.mkdir(parents=True)

    template_map(custom_role_dir, dest, d)


def generate_ansible(build_dir, config):
    build_root = Path(build_dir)
    ansible_dir = build_root / 'ansible'

    workchain_cfg = config['wrkchain']
    bootnode_cfg = workchain_cfg['bootnode']

    bootnode = Bootnode(bootnode_cfg)
    custom_roles = ['bash']
    validator_builder = Validators(workchain_cfg['nodes'], custom_roles)

    d = {
        'wrkchain-bootnode.yml': bootnode,
        'wrkchain-node.yml': validator_builder,
        'Vagrantfile': workchain_cfg
    }
    template_map(template_root() / 'ansible', ansible_dir, d)
    process_custom_roles(template_root(), ansible_dir,
                         transform_to_node_map(workchain_cfg))

    # Post Processing
    bootnode.link_bootnode_key(build_root)
    validator_builder.link_genesis(build_root)
