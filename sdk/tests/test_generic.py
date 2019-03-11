import glob
import os


test_genesis = {
  "config":{
    "chainId":209865847,
    "homesteadBlock":1,
    "eip150Block":2,
    "eip150Hash":"0x0000000000000000000000000000000000000000000000000000000000000000",
    "eip155Block":3,
    "eip158Block":3,
    "byzantiumBlock":4,
    "constantinopleBlock":5,
    "clique":{
      "period":5,
      "epoch":30000
    }
  },
  "nonce":"0x0",
  "timestamp":"0x5c7fce99",
  "extraData":"0000000000000000000000000000000033756c26e881b64B993D3FeC57b1cDCa8Bf5d20aDccc523747B80c56cdF45aF1aB8bc6E9234b59F900000000000000000000000000000000000000000000000000000000000000000",
  "gasLimit":"0x2cd29c0",
  "difficulty":"0x1",
  "mixHash":"0x0000000000000000000000000000000000000000000000000000000000000000",
  "coinbase":"0x0000000000000000000000000000000000000000",
  "number":"0x0",
  "gasUsed":"0x0",
  "parentHash":"0x0000000000000000000000000000000000000000000000000000000000000000",
  "alloc":{
    "015d1CBC280a455885b98DD6e5C5C173ad45B366":{
      "balance":"0x33b2e3c9fd0803ce8000000"
    }
  }
}

test_config = {
   "workchain":{
      "title":"Example Workchain",
      "ledger":{
          "base": "geth",
          "consensus": {
              "type": "clique",
              "period": 5,
              "epoch": 30000
          },
          "permission": "public"
      },
      "bootnode": {
        "use": True,
        "ip": "127.0.0.1",
        "port": "30301"
      },
      "validators":[
          {
              "address": "0xA6ac533Bd51cc4c8BB0c72612669c62B35521578",
              "private_key": "7deeb75a3bbaa57bc073380b77f47d701d7e2ef7551719f3767d4eee0a5fdffd",
              "write_to_oracle": True
          },
          {
              "address": "0xC1DA2B192821b7BbcCFFCd9f3806b48af86f6EeA",
              "private_key": "b7459e3be8b6825ac1b606d5f4ac61652e04086f0645d7f768b5e1a176afffcf",
              "write_to_oracle": True
          }
      ],
      "rpc_nodes": [
          {
              "address": "0x46eE44d01531371312c3BeC9198277e3F5474106",
              "private_key": "d20e5beffa72c117498daf80140c15494c06dcc0fa4c61db7c6fff16572d78d5",
              "write_to_oracle": False
          }
      ],
      "coin": {
          "symbol": "COIN",
          "prefund": [
              {
                  "address": "0x015d1CBC280a455885b98DD6e5C5C173ad45B366",
                  "balance": "1000000000"
              }
          ]
      }
   },
   "mainchain": {
     "network": "testnet",
     "network_id": 50005,
     "web3_provider": {
       "type": "http",
       "uri": "http://52.14.173.249:8101"
     }
   }
}


def examples():
    from workchain_sdk.utils import repo_root
    examples_path = repo_root() / 'examples'
    query = os.path.join(str(examples_path), "*.json")
    config_files = glob.glob(query)
    return config_files


def test_parse_config():
    from workchain_sdk.config import parse_config

    config_files = examples()
    assert len(config_files) > 0

    for f in config_files:
        config = parse_config(f)
        print(config)


def test_composer():
    from workchain_sdk.composer import generate
    from workchain_sdk.genesis import DEFAULT_NETWORK_ID
    generate(test_config, 'BOOTNODE_ADDRESS', DEFAULT_NETWORK_ID)


def test_generate_documentation():
    from workchain_sdk.config import generate_documentation
    documentation = generate_documentation(test_config, test_genesis)
    print(documentation)
    assert len(documentation['md']) > 0
    assert len(documentation['html']) > 0


def test_generate_genesis():
    from workchain_sdk.config import generate_genesis

    genesis_json, workchain_id = generate_genesis(test_config)
    print(genesis_json)
    assert len(genesis_json) > 0
    assert workchain_id > 0
