import glob
import os
import pytest

from pathlib import Path

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
  "wrkchain":{
    "title":"Example WRKChain",
    "wrkchain_network_id":6450628417,
    "ledger":{
      "base":"geth",
      "consensus":{
        "type":"clique",
        "period":5,
        "epoch":30000
      },
      "permission":"public"
    },
    "bootnode":{
      "use":True,
      "ip":"172.25.0.2",
      "port":30304
    },
    "chaintest":False,
    "nodes":[
      {
        "id":"Validator UK",
        "address":"0xA6ac533Bd51cc4c8BB0c72612669c62B35521578",
        "private_key":"7deeb75a3bbaa57bc073380b77f47d701d7e2ef7551719f3767d4eee0a5fdffd",
        "ip":"172.25.0.4",
        "listen_port":30302,
        "is_validator":True,
        "write_to_oracle":True,
        "rpc":False
      },
      {
        "id":"Validator US",
        "address":"0xC1DA2B192821b7BbcCFFCd9f3806b48af86f6EeA",
        "private_key":"b7459e3be8b6825ac1b606d5f4ac61652e04086f0645d7f768b5e1a176afffcf",
        "ip":"172.25.0.5",
        "listen_port":30303,
        "is_validator":True,
        "write_to_oracle":True,
        "rpc":False
      },
      {
        "id":"JSON-RPC Node",
        "address":"0x46eE44d01531371312c3BeC9198277e3F5474106",
        "private_key":"d20e5beffa72c117498daf80140c15494c06dcc0fa4c61db7c6fff16572d78d5",
        "ip":"172.25.0.6",
        "listen_port":30304,
        "is_validator":False,
        "write_to_oracle":False,
        "rpc":{
          "port":8545,
          "apis":{
            "eth":True,
            "web3":True,
            "net":True,
            "admin":True,
            "debug":True,
            "db":True,
            "personal":False,
            "miner":False,
            "ssh":False,
            "txpool":False
          }
        }
      }
    ],
    "coin":{
      "symbol":"COIN",
      "prefund":[
        {
          "address":"0xfBf151E90436beC94DA59D0D4f434C9Ea6CC40Cd",
          "balance":"1000000000"
        }
      ]
    }
  },
  "mainchain":{
    "network":"testnet",
    "network_id":50005,
    "web3_provider":{
      "type":"http",
      "uri":"http://52.14.173.249:8101",
      "host":"52.14.173.249",
      "port":"8101"
    }
  }
}

static_bootnode_config = {'type': 'static', 'nodes': {'0xA6ac533Bd51cc4c8BB0c72612669c62B35521578': {'address': 'ded1316f6b52d83675cbd20593b76f5f82d98dae23e01505728abfd4d1d63b58577891d6b2cfcd07c735460cfa857f2cb58a6800cb6c3b2ac9805940630c393d', 'enode': 'enode://ded1316f6b52d83675cbd20593b76f5f82d98dae23e01505728abfd4d1d63b58577891d6b2cfcd07c735460cfa857f2cb58a6800cb6c3b2ac9805940630c393d@127.0.0.1:30303', 'ip': '127.0.0.1', 'port': 30303}, '0xC1DA2B192821b7BbcCFFCd9f3806b48af86f6EeA': {'address': '27d2cde435562fe176e185510a3c748b692c311102a060d1b6ed1be7e02ce4679dea02a50cc60d60d80074c5635f4dab69d82d83406690c88d58c01d41534407', 'enode': 'enode://27d2cde435562fe176e185510a3c748b692c311102a060d1b6ed1be7e02ce4679dea02a50cc60d60d80074c5635f4dab69d82d83406690c88d58c01d41534407@127.0.0.1:30302', 'ip': '127.0.0.1', 'port': 30302}, '0x46eE44d01531371312c3BeC9198277e3F5474106': {'address': '8db8bd50335abccfb746c9584c526f07a7939983bfec8329abfbba19cd29adc6514927f5eb51fa8d8ccaa321afae03391f64a7566256ebe709cb1cc212afd710', 'enode': 'enode://8db8bd50335abccfb746c9584c526f07a7939983bfec8329abfbba19cd29adc6514927f5eb51fa8d8ccaa321afae03391f64a7566256ebe709cb1cc212afd710@127.0.0.1:30303', 'ip': '127.0.0.1', 'port': 30303}}}
bootnode_config = {'type': 'dedicated', 'nodes': {'address': 'c6a2c2dcdc7ba6e6a5db5e138cf7ba6dfb75d92e28d3f7267ee297150696c4c5a8172e004e2bf29e30b8abb4ebe27c9a3dc48cfa908792801bcf9080557257a6', 'enode': 'enode://c6a2c2dcdc7ba6e6a5db5e138cf7ba6dfb75d92e28d3f7267ee297150696c4c5a8172e004e2bf29e30b8abb4ebe27c9a3dc48cfa908792801bcf9080557257a6@127.0.0.1:30304', 'ip': '127.0.0.1', 'port': 30304}}


def examples():
    current_script = Path(os.path.abspath(__file__))
    examples_path = current_script.parent / 'test_data'
    query = os.path.join(str(examples_path), "*.json")
    config_files = glob.glob(query)
    return config_files


def fail_examples(prefix):
    current_script = Path(os.path.abspath(__file__))
    examples_path = current_script.parent / 'test_data' / 'should_fail'
    query = os.path.join(str(examples_path), prefix + "*.json")
    config_files = glob.glob(query)
    return config_files


def check_overrides_in_config(overrides, config):
    for key, data in overrides.items():
        if isinstance(data, dict):
            check_overrides_in_config(data, config[key])
        elif isinstance(data, list):
            for i in range(len(data)):
                ov = data[i]
                co = config[key][i]
                if isinstance(ov, dict):
                    check_overrides_in_config(ov, co)
        else:
            if key == 'rpc' and isinstance(data, bool):
                continue
            else:
                assert data == config[key]


def test_parse_config():
    from wrkchain.config import WRKChainConfig

    config_files = examples()
    assert len(config_files) > 0

    for f in config_files:
        wrkchain_config = WRKChainConfig(f)
        config = wrkchain_config.get()
        print(config)


def test_parse_config_missing_nodes():
    from wrkchain.config import WRKChainConfig, \
        MissingConfigOverrideException

    config_files = fail_examples('nodes_')
    assert len(config_files) > 0

    for f in config_files:
        with pytest.raises(MissingConfigOverrideException):
            # should fail - missing nodes
            WRKChainConfig(f)


def test_parse_config_missing_mainchain():
    from wrkchain.config import WRKChainConfig, \
        MissingConfigOverrideException

    config_files = fail_examples('mainchain_')
    assert len(config_files) > 0

    for f in config_files:
        with pytest.raises(MissingConfigOverrideException):
            # should fail - invalid mainchain config
            WRKChainConfig(f)


def test_parse_config_invalid_addresses():
    from wrkchain.config import WRKChainConfig, \
        InvalidOverrideException

    config_files = fail_examples('address_')
    assert len(config_files) > 0

    for f in config_files:
        with pytest.raises(InvalidOverrideException):
            # should fail - invalid mainchain config
            WRKChainConfig(f)


def test_successful_override():
    from wrkchain.config import WRKChainConfig

    config_files = examples()
    assert len(config_files) > 0

    for f in config_files:
        wrkchain_config = WRKChainConfig(f)
        config = wrkchain_config.get()
        override = wrkchain_config.get_overrides()
        check_overrides_in_config(override, config)


def test_composer():
    from wrkchain.composer import generate
    from wrkchain.genesis import DEFAULT_NETWORK_ID
    from wrkchain.sdk import configure_bootnode
    build_dir = '/tmp'
    bootnode_cfg = configure_bootnode(build_dir, test_config)
    generate(test_config, bootnode_cfg, DEFAULT_NETWORK_ID)


def test_generate_documentation():
    from wrkchain.sdk import generate_documentation
    build_dir = '/tmp'
    documentation = generate_documentation(test_config, test_genesis,
                                           bootnode_config, build_dir)
    print(documentation)
    assert len(documentation['md']) > 0
    assert len(documentation['html']) > 0


def test_generate_documentation_no_bootnode():
    build_dir = '/tmp'
    from wrkchain.sdk import generate_documentation
    test_config['wrkchain']['bootnode']['use'] = False
    documentation = generate_documentation(test_config, test_genesis,
                                           static_bootnode_config, build_dir)
    print(documentation)
    assert len(documentation['md']) > 0
    assert len(documentation['html']) > 0


def test_generate_genesis():
    from wrkchain.sdk import generate_genesis

    genesis_json, wrkchain_id = generate_genesis(test_config)
    print(genesis_json)
    assert len(genesis_json) > 0
    assert wrkchain_id > 0
