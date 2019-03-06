import glob
import json
import os

from pathlib import Path


def examples():
    current_script = Path(os.path.abspath(__file__))
    examples_path = current_script.parent.parent.parent / 'examples'
    query = os.path.join(examples_path, "*.json")
    config_files = glob.glob(query)
    return config_files


def example_addresses():
    addresses = [
        '0xDccc523747B80c56cdF45aF1aB8bc6E9234b59F9'
    ]
    return addresses


def get_conf(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)

    return d


def test_check_und_funds():
    from workchain_sdk.mainchain import UndMainchain

    addresses = example_addresses()
    assert len(addresses) > 0

    config_files = examples()
    assert len(config_files) > 0

    for config_file in config_files:
        d = get_conf(config_file)
        network = d['mainchain']['network']
        web3_type = d['mainchain']['web3_provider']['type']
        web3_uri = d['mainchain']['web3_provider']['uri']
        und_mainchain = UndMainchain(network=network,
                                     web3_type=web3_type,
                                     web3_uri=web3_uri)
        for address in addresses:
            current_balance = und_mainchain.check_und_funds(address)
            assert current_balance >= 0
