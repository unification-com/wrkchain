import click
import json
import logging

from workchain.bootnode import BootnodeKey
from workchain.composer import generate
from workchain.documentation.documentation import WorkchainDocumentation
from workchain.genesis import build_genesis, generate_workchain_id
from workchain.mainchain import UndMainchain
from workchain.utils import write_build_file, get_oracle_addresses

log = logging.getLogger(__name__)


def parse_config(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)

    return d


def generate_documentation(config, genesis_json, bootnode_config):
    doc_gen = WorkchainDocumentation(config,
                                     genesis_json['config']['chainId'],
                                     bootnode_config)
    doc_gen.generate()

    documentation = {
        'md': doc_gen.get_md(),
        'html': doc_gen.get_html()
    }

    return documentation


def generate_genesis(config):
    block_period = config['workchain']['ledger']['consensus']['period']
    validators = config['workchain']['validators']
    pre_funded_accounts = config['workchain']['coin']['prefund']

    workchain_base = config['workchain']['ledger']['base']
    workchain_consensus = config['workchain']['ledger']['consensus']['type']
    workchain_id = generate_workchain_id()

    genesis_json = build_genesis(
        block_period=block_period,  validators=validators,
        workchain_base=workchain_base,
        workchain_consensus=workchain_consensus,
        workchain_id=workchain_id,
        pre_funded_accounts=pre_funded_accounts)

    return genesis_json, workchain_id


def write_genesis(build_dir, genesis_json):
    write_build_file(build_dir + '/genesis.json', genesis_json)


def write_documentation(build_dir, documentation):
    write_build_file(build_dir + '/README.md', documentation['md'])
    write_build_file(build_dir + '/documentation.html',
                     documentation['html'])


def write_composition(build_dir, composition):
    write_build_file(build_dir + '/docker-compose.yml', composition)


def write_static_nodes(build_dir, static_nodes):
    write_build_file(build_dir + '/static-nodes.json', static_nodes)


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
                       f'Workchain Root smart contract')


def configure_bootnode(build_dir, config):
    bootnode_config = {}
    if config['workchain']['bootnode']['use']:
        node_info = {}
        ip = config['workchain']['bootnode']['ip']
        port = config['workchain']['bootnode']['port']
        bootnode_key = BootnodeKey(build_dir, ip, port)
        bootnode_address = bootnode_key.get_bootnode_address()

        node_info['address'] = bootnode_address
        node_info['enode'] = bootnode_key.get_enode()
        node_info['ip'] = ip
        node_info['port'] = port

        bootnode_config['type'] = 'dedicated'
        bootnode_config['nodes'] = node_info
    else:
        validators = config['workchain']['validators']
        nodes = {}
        static_addresses_list = []

        for validator in validators:
            node_info = {}
            public_address = validator['address']
            ip = validator['ip']
            port = validator['listen_port']
            bootnode_key = BootnodeKey(build_dir, ip, port,
                                       f'{public_address}_')
            bootnode_address = bootnode_key.get_bootnode_address()
            enode = bootnode_key.get_enode()

            node_info['address'] = bootnode_address
            node_info['enode'] = enode
            node_info['ip'] = ip
            node_info['port'] = port

            nodes[public_address] = node_info

            static_addresses_list.append(enode)

        bootnode_config['type'] = 'static'
        bootnode_config['nodes'] = nodes

        rendered_static_nodes = json.dumps(static_addresses_list,
                                           indent=2, separators=(',', ':'))
        write_static_nodes(build_dir, rendered_static_nodes)

    return bootnode_config


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
@click.argument('build_dir')
def generate_workchain(config_file, build_dir):
    log.info(f'Generating environment from: {config_file}')
    config = parse_config(config_file)

    genesis_json, workchain_id = generate_genesis(config)
    bootnode_address = None
    bootnode_config = configure_bootnode(build_dir, config)

    if config['workchain']['bootnode']['use']:
        ip = config['workchain']['bootnode']['ip']
        port = config['workchain']['bootnode']['port']
        bootnode_key = BootnodeKey(build_dir, ip, port)
        bootnode_address = bootnode_key.get_bootnode_address()
        click.echo(f'Bootnode Address: {bootnode_address}')

    documentation = generate_documentation(config, genesis_json,
                                           bootnode_config)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))
    composition = generate(config, bootnode_address, workchain_id)

    write_genesis(build_dir, rendered)
    write_documentation(build_dir, documentation)
    write_composition(build_dir, composition)

    click.echo(documentation['md'])
    click.echo(rendered)
    click.echo(composition)
    click.echo(bootnode_config)


if __name__ == "__main__":
    main()
