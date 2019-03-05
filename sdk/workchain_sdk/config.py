import json
import logging

import click

from workchain_sdk.genesis import build_genesis

log = logging.getLogger(__name__)



def check_valid(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
def validate(config_file):
    log.info(f'Validating: {config_file}')
    check_valid(config_file)
    build_genesis()


if __name__ == "__main__":
    main()
