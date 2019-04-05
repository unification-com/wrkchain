from os import path, symlink, unlink
from pathlib import Path
from shutil import copy

from ansible.parsing.dataloader import DataLoader
from ansible.parsing.vault import FileVaultSecret, VaultLib
from jinja2 import DebugUndefined, Environment, FileSystemLoader

from wrkchain.architectures.debian import generate_geth_cmd
from wrkchain.constants import (
    GO_VERSION, WALLET_PASSWORD, PASSWORD_FILE, DEFAULT_WRKCHAIN_DATA_DIR)
from wrkchain.keys import generate_ssh_keys
from wrkchain.utils import template_root


def relative_symlink(build_root, src_dir: str, dst_dir: str, filename):
    """

    :param src_dir: Directory path fragment. Use / for none.
    :param dst_dir: Directory path fragment. Use / for none.
    :return:
    """
    build_root_full_path = Path(path.abspath(build_root))
    if src_dir != '/':
        src_dir = build_root_full_path / src_dir
    else:
        src_dir = build_root_full_path

    if dst_dir != '/':
        dst_dir = build_root_full_path / dst_dir
    else:
        dst_dir = build_root_full_path

    rel_src_dir = Path(path.relpath(src_dir, dst_dir))
    dst = dst_dir / filename
    src = rel_src_dir / filename

    if dst.exists():
        unlink(dst)
    symlink(src, dst)


def encrypt_string(passwordfile, var_name, plain_text):
    loader = DataLoader()
    secret = FileVaultSecret(
        filename=passwordfile, encoding='utf8', loader=loader)
    secret.load()

    encrypt_vault_id = 'default'
    encrypt_secret = secret

    vault_secrets = [(encrypt_vault_id, encrypt_secret)]

    vault = VaultLib(vault_secrets)
    b_vaulttext = vault.encrypt(
        plain_text, secret=secret, vault_id=encrypt_vault_id)
    code = b_vaulttext.decode()

    code = code.rstrip()
    code = code.replace("\n", "\n      ")

    return f"{var_name}: !vault |\n      {code}"


class Validators:
    def __init__(self, build_dir, context, custom_roles):
        self.build_dir = build_dir
        self.context = context
        self.custom_roles = custom_roles

    def role_name(self, name, key):
        return f"{name}_{key}"

    def write(self, environment, target, relative):
        template = environment.get_template(str(relative))
        for index, validator in enumerate(self.context):
            base, ext = str(relative).split('.')
            dest = target / f'{base}-{index + 1}.{ext}'

            ps = sorted([
                ("private_key", validator['private_key']),
                ("password", WALLET_PASSWORD)
            ])
            password_file = self.build_dir / 'ansible' / PASSWORD_FILE

            eff = {
                'vars': [
                    encrypt_string(password_file, x[0], x[1]) for x in ps],
                'custom_roles': [self.role_name(x, validator['name']) for x in
                                 self.custom_roles],
                'optional_roles': ['oracle'] if validator[
                    'write_to_oracle'] else [],
                'validator': validator
            }
            dest.write_text(template.render(eff))

    def link_genesis(self, build_root):
        relative_symlink(
            build_root, '/', 'ansible/roles/node/files/', 'genesis.json')


class Bootnode:
    def __init__(self, context):
        self.context = context

    def write(self, environment, target, relative):
        if self.context['use']:
            template = environment.get_template(str(relative))
            dest = target / str(relative)
            dest.write_text(template.render(self.context))

    def link_bootnode_key(self, build_root):
        if self.context['use']:
            relative_symlink(
                build_root, 'node_keys', 'ansible/roles/bootnode/files/',
                'bootnode.key')


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


def transform_to_node_map(wrkchain_cfg):
    ret = {}
    for node in wrkchain_cfg['nodes']:
        ret[node['name']] = node
    return ret


def inject_geth_command(bootnode_config, wrkchain_id, workchain_nodes):
    for key, validator in workchain_nodes.items():
        cmd = generate_geth_cmd(
            validator, bootnode_config, wrkchain_id,
            validator['docker_listen_port'])
        validator['geth_command'] = cmd
    return workchain_nodes


def process_custom_roles(template_root, ansible_dir, node_map):
    source = template_root / 'ansible' / 'custom_roles'

    for path in [x for x in source.glob('*') if x.is_dir()]:
        role_name = path.name

        for node, node_d in node_map.items():
            d = {
                'files/motd': node_d,
                'templates/geth.service': node_d,
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


def write_keys(build_root: Path, name: str):
    private_key, public_key = generate_ssh_keys()

    target_private = build_root / 'ssh_keys' / f'{name}'
    if not target_private.parent.exists():
        target_private.parent.mkdir(parents=True)

    target_private.write_bytes(private_key)
    target_private.chmod(0o600)

    target_public = build_root / 'ssh_keys' / f'{name}.pub'
    target_public.write_bytes(public_key)
    target_public.chmod(0o600)


def generate_ansible(build_dir, config, configured_bootnode_cfg):
    build_root = Path(build_dir)

    ansible_dir = build_root / 'ansible'

    wrkchain_cfg = config['wrkchain']
    bootnode = Bootnode(wrkchain_cfg['bootnode'])
    validator_builder = Validators(
        build_root, wrkchain_cfg['nodes'], ['bash', 'services'])

    # copy the password file before all else
    password_file = template_root() / 'ansible' / PASSWORD_FILE
    if not ansible_dir.exists():
        ansible_dir.mkdir(parents=True)

    # Generate some keys pairs
    write_keys(build_root, 'id_rsa_root')
    write_keys(build_root, 'id_rsa_deploy')

    copy(str(password_file), str(ansible_dir / PASSWORD_FILE))

    d = {
        'roles/ethereum/tasks/main.yml': {'go_version': GO_VERSION,
                                          'wrkchain_data_dir':
                                              DEFAULT_WRKCHAIN_DATA_DIR},
        'roles/node/tasks/account.yml': {'wrkchain_data_dir':
                                              DEFAULT_WRKCHAIN_DATA_DIR},
        'roles/node/tasks/main.yml': {'wrkchain_data_dir':
                                              DEFAULT_WRKCHAIN_DATA_DIR},
        '/roles/bootnode/tasks/main.yml': {'wrkchain_data_dir':
                                              DEFAULT_WRKCHAIN_DATA_DIR},
        'wrkchain-bootnode.yml': bootnode,
        'wrkchain-node.yml': validator_builder,
        'Vagrantfile': wrkchain_cfg
    }
    template_map(template_root() / 'ansible', ansible_dir, d)

    network_id = config['wrkchain']['wrkchain_network_id']
    node_map = transform_to_node_map(wrkchain_cfg)
    workchain_nodes = inject_geth_command(
        configured_bootnode_cfg, network_id, node_map)
    process_custom_roles(template_root(), ansible_dir, workchain_nodes)

    # Post Processing
    bootnode.link_bootnode_key(build_root)
    validator_builder.link_genesis(build_root)

    relative_symlink(
        build_root, 'ssh_keys', 'ansible/roles/base/files/',
        'id_rsa_deploy.pub')

    relative_symlink(
        build_root, 'ssh_keys', 'ansible/roles/base/files/',
        'id_rsa_root.pub')
