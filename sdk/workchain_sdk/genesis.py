from datetime import datetime
from random import SystemRandom

from web3.auto import w3


clique_template = {
    "config": {
        "chainId": None,
        "homesteadBlock": 1,
        "eip150Block": 2,
        "eip150Hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "eip155Block": 3,
        "eip158Block": 3,
        "byzantiumBlock": 4,
        "constantinopleBlock": 5,
        "clique": {
            "period": None,
            "epoch": 30000
        }
    },
    "nonce": "0x0",
    "timestamp": None,
    "extraData": None,
    "gasLimit": "0x2cd29c0",
    "difficulty": "0x1",
    "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": "0x0000000000000000000000000000000000000000",
    "number": "0x0",
    "gasUsed": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
}


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
    return f"{'0'*32}{''.join(addresses)}{'0'*65}"


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


def build_genesis(block_period, validators, pre_funded_accounts=None):
    t = clique_template
    t['config']['chainId'] = generate_workchain_id()
    t['config']['clique']['period'] = block_period
    t['extraData'] = build_extra_data(validators)
    t['timestamp'] = generate_timestamp()

    if pre_funded_accounts:
        t['alloc'] = pre_fund(pre_funded_accounts)

    return t
