clique_template = {
    "config": {
        "chainId": 50002,
        "homesteadBlock": 1,
        "eip150Block": 2,
        "eip150Hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "eip155Block": 3,
        "eip158Block": 3,
        "byzantiumBlock": 4,
        "constantinopleBlock": 5,
        "clique": {
            "period": 5,
            "epoch": 30000
        }
    },
    "nonce": "0x0",
    "timestamp": "0x5c49efa1",
    "extraData": "",
    "gasLimit": "0x2cd29c0",
    "difficulty": "0x1",
    "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": "0x0000000000000000000000000000000000000000",
    "number": "0x0",
    "gasUsed": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
}


def build_genesis(mainchain_network_id, block_period):
    t = clique_template
    t['config']['chainId'] = mainchain_network_id
    t['config']['clique']['period'] = block_period
    return t
