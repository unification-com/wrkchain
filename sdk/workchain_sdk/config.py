import json
import logging
import os

import click

from workchain_sdk.composer import generate
from workchain_sdk.documentation import WorkchainDocumentation
from workchain_sdk.genesis import build_genesis

log = logging.getLogger(__name__)


def parse_config(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)

    return d


def generate_readme(config, genesis_json):
    doc_gen = WorkchainDocumentation(config, genesis_json['config']['chainId'])
    readme = doc_gen.generate()
    return readme


def generate_genesis(config):
    block_period = config['workchain']['ledger']['consensus']['period']
    validators = config['workchain']['validators']
    pre_funded_accounts = config['workchain']['coin']['prefund']

    workchain_base = config['workchain']['ledger']['base']
    workchain_consensus = config['workchain']['ledger']['consensus']['type']

    genesis_json = build_genesis(
        block_period=block_period, validators=validators,
        workchain_base=workchain_base,
        workchain_consensus=workchain_consensus,
        pre_funded_accounts=pre_funded_accounts)

    return genesis_json


def write_genesis(build_dir, genesis_json):
    genesis_file = open(build_dir + "/genesis.json", "w")
    genesis_file.write(genesis_json)
    genesis_file.close()
    os.chmod(build_dir + '/genesis.json', 0o666)


def write_readme(build_dir, readme):
    readme_file = open(build_dir + "/README.md", "w")
    readme_file.write(readme)
    readme_file.close()

    os.chmod(build_dir + '/README.md', 0o666)


def write_composition(build_dir, composition):
    readme_file = open(build_dir + "/docker-compose.yml", "w")
    readme_file.write(composition)
    readme_file.close()
    os.chmod(build_dir + '/docker-compose.yml', 0o666)


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
@click.argument('build_dir')
def validate(config_file, build_dir):
    log.info(f'Validating: {config_file}')
    config = parse_config(config_file)

    genesis_json = generate_genesis(config)
    readme = generate_readme(config, genesis_json)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))
    composition = generate()

    write_genesis(build_dir, rendered)
    write_readme(build_dir, readme)
    write_composition(build_dir, composition)

    click.echo(rendered)
    click.echo(composition)


if __name__ == "__main__":
    main()
