import click
import json
import logging

from workchain_sdk.bootnode import BootnodeKey
from workchain_sdk.composer import generate
from workchain_sdk.documentation.documentation import WorkchainDocumentation
from workchain_sdk.genesis import build_genesis, generate_workchain_id
from workchain_sdk.mainchain import UndMainchain
from workchain_sdk.utils import write_build_file, get_oracle_addresses

log = logging.getLogger(__name__)


def parse_config(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)

    return d


def generate_documentation(config, genesis_json, bootnode_address=None):
    doc_gen = WorkchainDocumentation(config,
                                     genesis_json['config']['chainId'],
                                     bootnode_address=bootnode_address)
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

    if config['workchain']['bootnode']['use']:
        bootnode_key = BootnodeKey(build_dir)
        bootnode_address = bootnode_key.get_bootnode_address()
        click.echo(f'Bootnode Address: {bootnode_address}')

    documentation = generate_documentation(config, genesis_json,
                                           bootnode_address)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))
    composition = generate(config, bootnode_address, workchain_id)

    write_genesis(build_dir, rendered)
    write_documentation(build_dir, documentation)
    write_composition(build_dir, composition)

    click.echo(documentation['md'])
    click.echo(rendered)
    click.echo(composition)


if __name__ == "__main__":
    main()
