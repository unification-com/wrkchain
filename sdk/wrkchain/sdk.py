import click
import json
import logging
import os

from pathlib import Path
from shutil import rmtree, copyfile

from wrkchain.ansible_generator import generate_ansible
from wrkchain.bootnode import BootnodeKey, BootnodeNotFoundException
from wrkchain.composer import generate
from wrkchain.config import (
    InvalidOverrideException, MissingConfigOverrideException, WRKChainConfig)
from wrkchain.documentation.documentation import WRKChainDocumentation
from wrkchain.genesis import build_genesis
from wrkchain.mainchain import UndMainchain
from wrkchain.utils import get_oracle_addresses, repo_root, write_build_file


log = logging.getLogger(__name__)


def generate_documentation(config, genesis_json, bootnode_config, build_dir):
    # derived from config
    wrkchain_name = config['wrkchain']['title']
    nodes = config['wrkchain']['nodes']
    mainchain_network = config["mainchain"]["network"]
    ledger_base_type = config["wrkchain"]["ledger"]["base"]
    oracle_addresses = get_oracle_addresses(config)
    mainchain_web3_provider = config['mainchain']['web3_provider']
    mainchain_network_id = config['mainchain']['network_id']
    oracle_write_frequency = config['wrkchain']['oracle_write_frequency']
    consensus = config["wrkchain"]["ledger"]["consensus"]["type"]

    # from genesis.json
    wrkchain_id = genesis_json['config']['chainId']

    wrkchain_documentation = WRKChainDocumentation(
        wrkchain_name, nodes, mainchain_network, ledger_base_type,
        oracle_addresses, mainchain_web3_provider, mainchain_network_id,
        wrkchain_id, bootnode_config, genesis_json, build_dir,
        oracle_write_frequency, consensus)
    wrkchain_documentation.generate()

    documentation = {
        'md': wrkchain_documentation.get_md(),
        'html': wrkchain_documentation.get_html()
    }

    return documentation


def generate_genesis(config):
    block_period = config['wrkchain']['ledger']['consensus']['period']
    nodes = config['wrkchain']['nodes']
    pre_funded_accounts = config['wrkchain']['coin']['prefund']

    wrkchain_base = config['wrkchain']['ledger']['base']
    wrkchain_consensus = config['wrkchain']['ledger']['consensus']['type']
    wrkchain_id = config['wrkchain']['wrkchain_network_id']

    genesis_json = build_genesis(
        block_period=block_period, validators=nodes,
        wrkchain_base=wrkchain_base,
        wrkchain_consensus=wrkchain_consensus,
        wrkchain_id=wrkchain_id,
        pre_funded_accounts=pre_funded_accounts)

    return genesis_json, wrkchain_id


def write_genesis(build_dir, genesis_json):
    write_build_file(build_dir + '/genesis.json', genesis_json)


def write_documentation(build_dir, documentation):
    write_build_file(build_dir + '/documentation.md', documentation['md'])
    write_build_file(build_dir + '/documentation.html',
                     documentation['html'])


def write_composition(build_dir, composition):
    write_build_file(build_dir + '/docker-compose.yml', composition)


def write_static_nodes(build_dir, static_nodes, static_nodes_docker):
    write_build_file(build_dir + '/static-nodes.json', static_nodes)
    docker_dir = build_dir + '/docker'
    if not os.path.exists(docker_dir):
        os.mkdir(docker_dir)
    write_build_file(build_dir + '/docker/static-nodes.json',
                     static_nodes_docker)


def write_generated_config(build_dir, config):
    rendered_config = json.dumps(config, indent=2, separators=(',', ':'))
    write_build_file(build_dir + '/generated_config.json', rendered_config)


def copy_readme(build_dir):
    readme_src = repo_root() / 'templates' / 'docs' / 'md' / 'README.md'
    readme_dst = Path(build_dir) / 'README.md'
    copyfile(readme_src, readme_dst)


def check_oracle_address_funds(config):
    oracle_addresses = get_oracle_addresses(config)
    network = config['mainchain']['network']
    web3_type = config['mainchain']['web3_provider']['type']
    web3_uri = config['mainchain']['web3_provider']['uri']
    und_mainchain = UndMainchain(network=network,
                                 web3_type=web3_type,
                                 web3_uri=web3_uri)
    for address in oracle_addresses:
        current_balance = und_mainchain.check_und_funds(address)
        if current_balance == 0:
            click.echo(f'WARNING: address {address} has 0 UND on {network}.'
                       f'Funds required for deployment and running of'
                       f'WRKchain Root smart contract')


def generate_bootnode_info(build_dir, ip, port, docker_ip, docker_port,
                           public_address=''):
    node_info = {}
    try:
        bootnode_key = BootnodeKey(build_dir, ip, port, docker_ip,
                               docker_port, public_address)
    except BootnodeNotFoundException as e:
        click.echo("SDK ERROR:")
        click.echo(e)
        exit()

    bootnode_address = bootnode_key.get_bootnode_address()

    node_info['address'] = bootnode_address
    node_info['enode'] = bootnode_key.get_enode()
    node_info['docker_enode'] = bootnode_key.get_docker_enode()
    node_info['ip'] = ip
    node_info['port'] = port
    node_info['docker_ip'] = docker_ip
    node_info['docker_port'] = docker_port

    return node_info


def configure_bootnode(build_dir, config):
    bootnode_config = {}
    nodes = {}
    static_addresses_list = []
    static_addresses_list_docker = []

    for item in config['wrkchain']['nodes']:
        public_address = item['address']
        ip = item['ip']
        port = item['listen_port']
        docker_ip = item['docker_ip']
        docker_port = item['docker_listen_port']

        node_info = generate_bootnode_info(build_dir, ip, port, docker_ip,
                                           docker_port, public_address)

        nodes[public_address] = node_info

        static_addresses_list.append(node_info['enode'])
        static_addresses_list_docker.append(node_info['docker_enode'])

    if config['wrkchain']['bootnode']['use']:
        ip = config['wrkchain']['bootnode']['ip']
        port = config['wrkchain']['bootnode']['port']
        docker_ip = config['wrkchain']['bootnode']['docker_ip']
        docker_port = config['wrkchain']['bootnode']['docker_port']
        node_info = generate_bootnode_info(build_dir, ip, port, docker_ip,
                                           docker_port)
        bootnode_type = 'dedicated'
        nodes = node_info
    else:
        bootnode_type = 'static'

    rendered_static_nodes = json.dumps(
            static_addresses_list, indent=2, separators=(',', ':'))
    rendered_static_nodes_docker = json.dumps(
            static_addresses_list_docker, indent=2, separators=(',', ':'))

    write_static_nodes(build_dir, rendered_static_nodes,
                       rendered_static_nodes_docker)

    bootnode_config['type'] = bootnode_type
    bootnode_config['nodes'] = nodes
    return bootnode_config


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
@click.argument('build_dir')
@click.option('--clean', type=bool, default=False)
@click.option('--host_build_dir', default=None)
def generate_wrkchain(config_file, build_dir, clean=False,
                      host_build_dir=None):
    log.info(f'Generating environment from: {config_file}')

    click.echo(f'Parsing {config_file}, and setting defaults')
    try:
        wrkchain_config = WRKChainConfig(config_file)
        config = wrkchain_config.get()
    except MissingConfigOverrideException as e:
        click.echo("SDK ERROR:")
        click.echo(e)
        exit()
    except InvalidOverrideException as e:
        click.echo("SDK ERROR:")
        click.echo(e)
        exit()

    if clean:
        rmtree(build_dir)

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    copy_readme(build_dir)

    write_generated_config(build_dir, config)

    click.echo("Generating genesis.json")
    genesis_json, wrkchain_id = generate_genesis(config)
    rendered_genesis = json.dumps(genesis_json, indent=2,
                                  separators=(',', ':'))
    write_genesis(build_dir, rendered_genesis)

    click.echo("Generating bootnode")
    bootnode_config = configure_bootnode(build_dir, config)

    click.echo("Generating docker-compose.yml")
    docker_composition = generate(config, bootnode_config, wrkchain_id)
    write_composition(build_dir, docker_composition)

    click.echo("Generating Ansible")
    generate_ansible(build_dir, config)

    click.echo("Generating documentation")
    documentation = generate_documentation(config, genesis_json,
                                           bootnode_config, build_dir)
    write_documentation(build_dir, documentation)

    info_build_dir = build_dir
    if host_build_dir:
        info_build_dir = host_build_dir
    click.echo(f'Done. Build files located in {info_build_dir}')
    click.echo(f'See {info_build_dir}/README.md')


if __name__ == "__main__":
    main()
