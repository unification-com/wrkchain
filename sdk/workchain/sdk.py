import click
import json
import logging

from workchain.bootnode import BootnodeKey
from workchain.composer import generate
from workchain.config import WorkchainConfig
from workchain.documentation.documentation import WorkchainDocumentation
from workchain.genesis import build_genesis, generate_workchain_id
from workchain.mainchain import UndMainchain
from workchain.utils import write_build_file, get_oracle_addresses

log = logging.getLogger(__name__)


def generate_documentation(config, genesis_json, bootnode_config):

    # derived from config
    workchain_name = config['workchain']['title']
    nodes = config['workchain']['nodes']
    mainchain_netork = config["mainchain"]["network"]
    ledger_base_type = config["workchain"]["ledger"]["base"]
    oracle_addresses = get_oracle_addresses(config)
    mainchain_web3_provider = config['mainchain']['web3_provider']
    mainchain_network_id = config['mainchain']['network_id']

    # from genesis.json
    workchain_id = genesis_json['config']['chainId']

    workchain_documentation = WorkchainDocumentation(workchain_name, nodes,
                                                     mainchain_netork,
                                                     ledger_base_type,
                                                     oracle_addresses,
                                                     mainchain_web3_provider,
                                                     mainchain_network_id,
                                                     workchain_id,
                                                     bootnode_config,
                                                     genesis_json)
    workchain_documentation.generate()

    documentation = {
        'md': workchain_documentation.get_md(),
        'html': workchain_documentation.get_html()
    }

    return documentation


def generate_genesis(config):
    block_period = config['workchain']['ledger']['consensus']['period']
    nodes = config['workchain']['nodes']
    pre_funded_accounts = config['workchain']['coin']['prefund']

    workchain_base = config['workchain']['ledger']['base']
    workchain_consensus = config['workchain']['ledger']['consensus']['type']
    workchain_id = generate_workchain_id()

    genesis_json = build_genesis(
        block_period=block_period,  validators=nodes,
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


def generate_bootnode_info(build_dir, ip, port, public_address=''):
    node_info = {}
    bootnode_key = BootnodeKey(build_dir, ip, port, public_address)
    bootnode_address = bootnode_key.get_bootnode_address()

    node_info['address'] = bootnode_address
    node_info['enode'] = bootnode_key.get_enode()
    node_info['ip'] = ip
    node_info['port'] = port

    return node_info


def configure_bootnode(build_dir, config):
    bootnode_config = {}
    if config['workchain']['bootnode']['use']:
        ip = config['workchain']['bootnode']['ip']
        port = config['workchain']['bootnode']['port']
        node_info = generate_bootnode_info(build_dir, ip, port)
        bootnode_config['type'] = 'dedicated'
        bootnode_config['nodes'] = node_info
    else:
        nodes = {}
        static_addresses_list = []

        for item in config['workchain']['nodes']:
            public_address = item['address']
            ip = item['ip']
            port = item['listen_port']

            node_info = generate_bootnode_info(build_dir, ip, port,
                                               public_address)

            nodes[public_address] = node_info
            static_addresses_list.append(node_info['enode'])

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
    workchain_config = WorkchainConfig(config_file)
    config = workchain_config.get()

    genesis_json, workchain_id = generate_genesis(config)
    bootnode_config = configure_bootnode(build_dir, config)

    documentation = generate_documentation(config, genesis_json,
                                           bootnode_config)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))

    composition = generate(config, bootnode_config, workchain_id)

    write_genesis(build_dir, rendered)
    write_documentation(build_dir, documentation)
    write_composition(build_dir, composition)

    click.echo(documentation['md'])
    click.echo(rendered)
    click.echo(composition)


if __name__ == "__main__":
    main()
