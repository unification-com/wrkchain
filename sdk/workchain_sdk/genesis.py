from random import SystemRandom
import time

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
    "extraData": "",
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
    timestamp = int(time.time())
    hex_timestamp = '0x{:02x}'.format(timestamp)
    return hex_timestamp


def build_genesis(block_period):
    t = clique_template
    t['config']['chainId'] = generate_workchain_id()
    t['config']['clique']['period'] = block_period
    t['timestamp'] = generate_timestamp()
    return t
