import json
import logging
import os

import click

from workchain_sdk.genesis import build_genesis

log = logging.getLogger(__name__)


def parse_config(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)

    block_period = d['workchain']['ledger']['consensus']['period']
    validators = d['workchain']['validators']
    pre_funded_accounts = d['workchain']['coin']['prefund']

    workchain_base = d['workchain']['ledger']['base']
    workchain_consensus = d['workchain']['ledger']['consensus']['type']

    genesis_json = build_genesis(
        block_period=block_period, validators=validators,
        workchain_base=workchain_base,
        workchain_consensus=workchain_consensus,
        pre_funded_accounts=pre_funded_accounts)

    return genesis_json


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
@click.argument('build_dir')
def validate(config_file, build_dir):
    log.info(f'Validating: {config_file}')
    genesis_json = parse_config(config_file)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))

    f = open(build_dir + "/genesis.json", "w")
    f.write(rendered)
    f.close()

    os.chmod(build_dir + '/genesis.json', 0o666)

    click.echo(rendered)


if __name__ == "__main__":
    main()
