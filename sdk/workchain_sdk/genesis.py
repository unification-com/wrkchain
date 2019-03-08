import json

from datetime import datetime
from random import SystemRandom
from web3.auto import w3
from workchain_sdk.utils import repo_root


def load_genesis_template(workchain_base, workchain_consensus):
    template_file = repo_root() / 'templates' / 'genesis' / workchain_base / \
                    f'{workchain_consensus}.json'

    with open(template_file, 'r') as f:
        contents = f.read()
        t = json.loads(contents)

    return t


def generate_workchain_id():
    sys_random = SystemRandom()
    return sys_random.randint(99999, 9999999999)


def generate_timestamp():
    timestamp = int(datetime.utcnow().strftime("%s"))
    hex_timestamp = '0x{:02x}'.format(timestamp)
    return hex_timestamp


def build_extra_data(validators):
    strip = lambda x: x[2:]
    addresses = [strip(x['address']) for x in validators]
    addresses.sort()
    return f"0x{'0'*(32*2)}{''.join(addresses)}{'0'*(65*2)}"


def pre_fund(pre_funded_accounts):
    alloc = {}

    for account in pre_funded_accounts:
        if w3.isAddress(account['address']) and int(account['balance']) > 0:
            address = account['address'][2:]

            balance_wei = w3.toWei(account['balance'], 'ether')
            alloc[address] = {
                "balance": w3.toHex(balance_wei)
            }

    return alloc


def build_genesis(block_period, validators,
                  workchain_base="geth",
                  workchain_consensus="clique",
                  pre_funded_accounts=None):
    t = load_genesis_template(workchain_base, workchain_consensus)
    t['config']['chainId'] = generate_workchain_id()
    t['config']['clique']['period'] = block_period
    t['extraData'] = build_extra_data(validators)
    t['timestamp'] = generate_timestamp()

    if pre_funded_accounts:
        t['alloc'] = pre_fund(pre_funded_accounts)

    return t
