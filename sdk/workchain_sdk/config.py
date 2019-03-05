import json
import logging

import click

from workchain_sdk.genesis import build_genesis

log = logging.getLogger(__name__)


def parse_config(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)

    block_period = d['workchain']['ledger']['consensus']['period']
    validators = d['workchain']['validators']

    genesis_json = build_genesis(
        block_period=block_period, validators=validators)

    return genesis_json


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
def validate(config_file):
    log.info(f'Validating: {config_file}')
    genesis_json = parse_config(config_file)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))
    click.echo(rendered)


if __name__ == "__main__":
    main()
