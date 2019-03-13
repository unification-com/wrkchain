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
      "chaintest": False,
      "validators":[
          {
              "address": "0xA6ac533Bd51cc4c8BB0c72612669c62B35521578",
              "private_key": "7deeb75a3bbaa57bc073380b77f47d701d7e2ef7551719f3767d4eee0a5fdffd",
              "write_to_oracle": True,
              "ip": "127.0.0.1",
              "listen_port": 30303
          },
          {
              "address": "0xC1DA2B192821b7BbcCFFCd9f3806b48af86f6EeA",
              "private_key": "b7459e3be8b6825ac1b606d5f4ac61652e04086f0645d7f768b5e1a176afffcf",
              "write_to_oracle": True,
              "ip": "127.0.0.1",
              "listen_port": 30302
          }
      ],
      "rpc_nodes": [
          {
              "address": "0x46eE44d01531371312c3BeC9198277e3F5474106",
              "private_key": "d20e5beffa72c117498daf80140c15494c06dcc0fa4c61db7c6fff16572d78d5",
              "write_to_oracle": False,
              "ip": "127.0.0.1",
              "listen_port": 30301,
              "rpc_port": 8545
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
       "uri": "http://52.14.173.249:8101",
       "host": "52.14.173.249",
       "port": "8101"
     }
   }
}

static_bootnode_config = {'type': 'static', 'nodes': {'0xA6ac533Bd51cc4c8BB0c72612669c62B35521578': {'address': 'ded1316f6b52d83675cbd20593b76f5f82d98dae23e01505728abfd4d1d63b58577891d6b2cfcd07c735460cfa857f2cb58a6800cb6c3b2ac9805940630c393d', 'enode': 'enode://ded1316f6b52d83675cbd20593b76f5f82d98dae23e01505728abfd4d1d63b58577891d6b2cfcd07c735460cfa857f2cb58a6800cb6c3b2ac9805940630c393d@127.0.0.1:30303', 'ip': '127.0.0.1', 'port': 30303}, '0xC1DA2B192821b7BbcCFFCd9f3806b48af86f6EeA': {'address': '27d2cde435562fe176e185510a3c748b692c311102a060d1b6ed1be7e02ce4679dea02a50cc60d60d80074c5635f4dab69d82d83406690c88d58c01d41534407', 'enode': 'enode://27d2cde435562fe176e185510a3c748b692c311102a060d1b6ed1be7e02ce4679dea02a50cc60d60d80074c5635f4dab69d82d83406690c88d58c01d41534407@127.0.0.1:30302', 'ip': '127.0.0.1', 'port': 30302}, '0x46eE44d01531371312c3BeC9198277e3F5474106': {'address': '8db8bd50335abccfb746c9584c526f07a7939983bfec8329abfbba19cd29adc6514927f5eb51fa8d8ccaa321afae03391f64a7566256ebe709cb1cc212afd710', 'enode': 'enode://8db8bd50335abccfb746c9584c526f07a7939983bfec8329abfbba19cd29adc6514927f5eb51fa8d8ccaa321afae03391f64a7566256ebe709cb1cc212afd710@127.0.0.1:30303', 'ip': '127.0.0.1', 'port': 30303}}}
bootnode_config = {'type': 'dedicated', 'nodes': {'address': 'c6a2c2dcdc7ba6e6a5db5e138cf7ba6dfb75d92e28d3f7267ee297150696c4c5a8172e004e2bf29e30b8abb4ebe27c9a3dc48cfa908792801bcf9080557257a6', 'enode': 'enode://c6a2c2dcdc7ba6e6a5db5e138cf7ba6dfb75d92e28d3f7267ee297150696c4c5a8172e004e2bf29e30b8abb4ebe27c9a3dc48cfa908792801bcf9080557257a6@127.0.0.1:30304', 'ip': '127.0.0.1', 'port': 30304}}


def examples():
    from workchain.utils import repo_root
    examples_path = repo_root() / 'examples'
    query = os.path.join(str(examples_path), "*.json")
    config_files = glob.glob(query)
    return config_files


def test_parse_config():
    from workchain.config import parse_config

    config_files = examples()
    assert len(config_files) > 0

    for f in config_files:
        config = parse_config(f)
        print(config)


def test_composer():
    from workchain.composer import generate
    from workchain.genesis import DEFAULT_NETWORK_ID
    from workchain.config import configure_bootnode
    build_dir = '/tmp'
    bootnode_cfg = configure_bootnode(build_dir, test_config)
    generate(test_config, bootnode_cfg, DEFAULT_NETWORK_ID)


def test_generate_documentation():
    from workchain.config import generate_documentation
    documentation = generate_documentation(test_config, test_genesis,
                                           bootnode_config)
    print(documentation)
    assert len(documentation['md']) > 0
    assert len(documentation['html']) > 0


def test_generate_documentation_no_bootnode():
    from workchain.config import generate_documentation
    test_config['workchain']['bootnode']['use'] = False
    documentation = generate_documentation(test_config, test_genesis,
                                           static_bootnode_config)
    print(documentation)
    assert len(documentation['md']) > 0
    assert len(documentation['html']) > 0


def test_generate_genesis():
    from workchain.config import generate_genesis

    genesis_json, workchain_id = generate_genesis(test_config)
    print(genesis_json)
    assert len(genesis_json) > 0
    assert workchain_id > 0
