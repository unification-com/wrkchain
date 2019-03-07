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
      "validators":[
          {
              "address": "0xDccc523747B80c56cdF45aF1aB8bc6E9234b59F9"
          },
          {
              "address": "0x33756c26e881b64B993D3FeC57b1cDCa8Bf5d20a"
          }
      ],
      "rpc_nodes": [
          {
              "address": "0x821aea9a577a9b44299b9c15c88cf3087f3b5544"
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
    generate()


def test_generate_documentation():
    from workchain_sdk.config import generate_readme
    readme = generate_readme(test_config, test_genesis)
    print(readme)
    assert len(readme) > 0


def test_generate_genesis():
    from workchain_sdk.config import generate_genesis

    genesis_json = generate_genesis(test_config)
    print(genesis_json)
    assert len(genesis_json) > 0
