import click
import json
import logging

from wrkchain.bootnode import BootnodeKey
from wrkchain.composer import generate
from wrkchain.config import WRKChainConfig, MissingConfigOverrideException, \
    InvalidOverrideException
from wrkchain.documentation.documentation import WRKChainDocumentation
from wrkchain.genesis import build_genesis, generate_wrkchain_id
from wrkchain.mainchain import UndMainchain
from wrkchain.utils import write_build_file, get_oracle_addresses

log = logging.getLogger(__name__)


def generate_documentation(config, genesis_json, bootnode_config):
    # derived from config
    wrkchain_name = config['wrkchain']['title']
    nodes = config['wrkchain']['nodes']
    mainchain_netork = config["mainchain"]["network"]
    ledger_base_type = config["wrkchain"]["ledger"]["base"]
    oracle_addresses = get_oracle_addresses(config)
    mainchain_web3_provider = config['mainchain']['web3_provider']
    mainchain_network_id = config['mainchain']['network_id']

    # from genesis.json
    wrkchain_id = genesis_json['config']['chainId']

    wrkchain_documentation = WRKChainDocumentation(wrkchain_name, nodes,
                                                   mainchain_netork,
                                                   ledger_base_type,
                                                   oracle_addresses,
                                                   mainchain_web3_provider,
                                                   mainchain_network_id,
                                                   wrkchain_id,
                                                   bootnode_config,
                                                   genesis_json)
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
    wrkchain_id = generate_wrkchain_id()

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
    if config['wrkchain']['bootnode']['use']:
        ip = config['wrkchain']['bootnode']['ip']
        port = config['wrkchain']['bootnode']['port']
        node_info = generate_bootnode_info(build_dir, ip, port)
        bootnode_config['type'] = 'dedicated'
        bootnode_config['nodes'] = node_info

    nodes = {}
    static_addresses_list = []

    for item in config['wrkchain']['nodes']:
        public_address = item['address']
        ip = item['ip']
        port = item['listen_port']

        node_info = generate_bootnode_info(build_dir, ip, port,
                                           public_address)

        nodes[public_address] = node_info

    static_addresses_list.append(node_info['enode'])

    bootnode_config['type'] = 'static'
    bootnode_config['nodes'] = nodes

    rendered_static_nodes = json.dumps(
        static_addresses_list, indent=2, separators=(',', ':'))

    write_static_nodes(build_dir, rendered_static_nodes)
    return bootnode_config


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
@click.argument('build_dir')
def generate_wrkchain(config_file, build_dir):
    log.info(f'Generating environment from: {config_file}')

    try:
        wrkchain_config = WRKChainConfig(config_file)
        config = wrkchain_config.get()
        wrkchain_config.print()
    except MissingConfigOverrideException as e:
        click.echo("SDK ERROR:")
        click.echo(e)
        exit()
    except InvalidOverrideException as e:
        click.echo("SDK ERROR:")
        click.echo(e)
        exit()

    genesis_json, wrkchain_id = generate_genesis(config)
    bootnode_config = configure_bootnode(build_dir, config)

    documentation = generate_documentation(config, genesis_json,
                                           bootnode_config)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))

    composition = generate(config, bootnode_config, wrkchain_id)

    write_genesis(build_dir, rendered)
    write_documentation(build_dir, documentation)
    write_composition(build_dir, composition)

    click.echo(documentation['md'])
    click.echo(rendered)
    click.echo(composition)


if __name__ == "__main__":
    main()
