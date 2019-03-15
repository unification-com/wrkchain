import json
import pprint

from web3 import Web3

REQUIRED_OVERRIDES = ['workchain', 'mainchain']
REQUIRED_WORKCHAIN_OVERRIDES = ['nodes']
REQUIRED_WORKCHAIN_NODE_OVERRIDES = ['address']
REQUIRED_MAINCHAIN_OVERRIDES = ['network']
VALID_MAINCHAIN_NETWORKS = ['testnet', 'mainnet']
VALID_RPC_APIS = ['admin', 'db', 'debug', 'eth', 'miner', 'net', 'personal',
                  'shh', 'txpool', 'web3']


class MissingConfigOverrideException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InvalidOverrideException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class WorkchainConfig:
    def __init__(self, config_file):
        self.__overrides = {}
        self.__config = {}

        with open(config_file, 'r') as f:
            contents = f.read()
            self.__overrides = json.loads(contents)

        self.__check_overrides(config_file)
        self.__load_basic_defaults()
        self.__load_overrides()

    def get(self):
        return self.__config

    def get_overrides(self):
        return self.__overrides

    def print(self):
        pprint.sorted = lambda x, key=None: x
        pprint.pprint(self.__config)

    def print_overrides(self):
        pprint.sorted = lambda x, key=None: x
        pprint.pprint(self.__overrides)

    def __check_overrides(self, config_file):

        for k in REQUIRED_OVERRIDES:
            if k not in self.__overrides.keys():
                err = f'"{k}" not defined in {config_file}. Must ' \
                    f'define {", ".join(REQUIRED_OVERRIDES)}'

                raise MissingConfigOverrideException(err)

        for k in REQUIRED_WORKCHAIN_OVERRIDES:
            if k not in self.__overrides['workchain'].keys():
                err = f'"{k}" not defined in {config_file}.'
                raise MissingConfigOverrideException(err)

        if len(self.__overrides['workchain']['nodes']) == 0:
            err = f'No nodes defined in {config_file}. You must define ' \
                f'at least one node'
            raise MissingConfigOverrideException(err)

        for i in range(len(self.__overrides['workchain']['nodes'])):
            for k in REQUIRED_WORKCHAIN_NODE_OVERRIDES:
                if k not in self.__overrides['workchain']['nodes'][i].keys():
                    err = f'"{k}" not defined in workchain -> nodes -> Node ' \
                        f'{i} section in {config_file}.'
                    raise MissingConfigOverrideException(err)

        for k in REQUIRED_MAINCHAIN_OVERRIDES:
            if k not in self.__overrides['mainchain'].keys():
                err = f'"{k}" not defined in {config_file}. Must ' \
                    f'define {", ".join(REQUIRED_MAINCHAIN_OVERRIDES)}'
                raise MissingConfigOverrideException(err)

        if self.__overrides['mainchain']['network'] \
            not in VALID_MAINCHAIN_NETWORKS:
            network = self.__overrides['mainchain']['network']
            err = f'Invalid Mainchain Network {network}. Must be one of: ' \
                f'{", ".join(VALID_MAINCHAIN_NETWORKS)}'
            raise MissingConfigOverrideException(err)

    def __load_basic_defaults(self):
        basic_default = {
            'workchain': {
                'title': 'My Workchain',
                'ledger': self.__load_default_ledger(),
                'bootnode': self.__load_default_bootnode(),
                'chaintest': False,
                'nodes': [],
                'coin': self.__load_default_coin()
            },
            'mainchain': self.__load_default_mainchain()
        }

        self.__config = basic_default

    def __load_overrides(self):
        workchain_overrides = self.__overrides['workchain']

        # Title
        if 'title' in workchain_overrides:
            self.__config['workchain']['title'] = workchain_overrides['title']

        # Ledger
        if 'ledger' in workchain_overrides:
            self.__override_ledger(workchain_overrides['ledger'])

        # Bootnode
        if 'bootnode' in workchain_overrides:
            self.__override_bootnode(workchain_overrides['bootnode'])

        # Chaintest
        if 'chaintest' in workchain_overrides:
            self.__config['workchain']['chaintest'] = \
                workchain_overrides['chaintest']

        # Nodes
        if 'nodes' in workchain_overrides:
            self.__override_nodes(workchain_overrides['nodes'])

        # Coin
        if 'coin' in workchain_overrides:
            self.__override_coin(workchain_overrides['coin'])

        # Mainchain
        if 'mainchain' in self.__overrides:
            mainchain_overrides = self.__overrides['mainchain']
            self.__override_mainchain(mainchain_overrides)

    def __override_ledger(self, ledger):
        # Todo - load according to selected base (geth, etc.)
        new_conf = self.__load_default_ledger()
        for key, data in ledger.items():
            # Todo - check and clean consensus
            new_conf[key] = data
        self.__config['workchain']['ledger'] = new_conf

    def __override_bootnode(self, bootnode_conf):

        new_conf = self.__load_default_bootnode()

        for key, data in bootnode_conf.items():
            new_conf[key] = data
        self.__config['workchain']['bootnode'] = new_conf

    def __override_nodes(self, nodes):
        defined_nodes = []
        node_num = 1
        for node in nodes:
            new_node = self.__load_default_node(node_num)

            # Todo - WAAAY too many levels...
            for key, data in node.items():
                if key == 'rpc':
                    if isinstance(data, bool):
                        if not data:
                            new_node[key] = False
                        else:
                            # defaults already loaded
                            continue
                    else:
                        for k, d in data.items():
                            if k == 'apis':
                                apis = {}
                                for api in VALID_RPC_APIS:
                                    if api in data[k]:
                                        apis[api] = data[k][api]
                                    else:
                                        apis[api] = False
                                new_node[key][k] = apis
                            else:
                                new_node[key][k] = d
                elif key == 'address':
                    if not Web3.isAddress(data):
                        err = f'workchain -> nodes -> {node_num - 1} -> ' \
                            f'address "{data}"" is not a valid address'
                        raise InvalidOverrideException(err)
                    new_node[key] = Web3.toChecksumAddress(data)
                else:
                    new_node[key] = data

            node_num += 1

            defined_nodes.append(new_node)

        self.__config['workchain']['nodes'] = defined_nodes

    def __override_coin(self, coin):
        if 'symbol' in coin:
            self.__config['workchain']['coin']['symbol'] = coin['symbol']
        if 'prefund' in coin:
            prefund = []
            for account in self.__overrides['workchain']['coin']['prefund']:
                if not Web3.isAddress(account['address']):
                    err = f'coin -> prefund -> {account["address"]} is not ' \
                        f'a valid address'
                    raise InvalidOverrideException(err)

                prefund_account = {
                    'address': Web3.toChecksumAddress(account["address"]),
                    'balance': account["balance"]
                }
                prefund.append(prefund_account)

            self.__config['workchain']['coin']['prefund'] = prefund
        else:
            # use address from nodes
            prefund_accounts = []
            for node in self.__config['workchain']['nodes']:
                account = {
                    'address': node['address'],
                    'balance': "1000000000"
                }
                prefund_accounts.append(account)
            self.__config['workchain']['coin']['prefund'] = prefund_accounts

    def __override_mainchain(self, mainchain):
        if 'network' in mainchain:
            network = mainchain['network']
        else:
            network = 'testnet'

        new_config = self.__load_default_mainchain(network)

        if 'web3_provider' in mainchain:
            # Todo - check and clean web3 values
            new_config['web3_provider'] = mainchain['web3_provider']

        self.__config['mainchain'] = new_config

    @staticmethod
    def __load_default_ledger():
        ledger = {
            "base": "geth",
            "consensus": {
                "type": "clique",
                "period": 5,
                "epoch": 30000
            },
            "permission": "public"
        }

        return ledger

    @staticmethod
    def __load_default_bootnode():
        bootnode = {
            "use": False,
            "ip": "172.25.0.2",
            "port": 30304
        }

        return bootnode

    @staticmethod
    def __load_default_node(node_num):
        node = {
            "id": f'Validator & JSON RPC {node_num}',
            "address": "",
            "private_key": "",
            "ip": "172.25.0.2",
            "listen_port": 30301,
            "is_validator": True,
            "write_to_oracle": True,
            "rpc": {
                "port": 8545,
                "apis": {
                    "eth": True,
                    "web3": True,
                    "net": True,
                    "admin": True,
                    "debug": True,
                    "db": True,
                    "personal": False,
                    "miner": False,
                    "ssh": False,
                    "txpool": False
                }
            }
        }
        return node

    @staticmethod
    def __load_default_coin():
        coin = {
            "symbol": "COIN",
            "prefund": []
        }
        return coin

    def __load_default_mainchain(self, network=None):
        if not network:
            network = 'testnet'

        mainchain = {
            "network": f'{network}',
            "network_id": self.__get_default_mainchain_id(network),
            "web3_provider": self.__get_default_web3_provider(network)
        }

        return mainchain

    @staticmethod
    def __get_default_mainchain_id(network=None):
        if network == 'mainnet':
            return 50000
        elif network == 'testnet':
            return 50005
        else:
            # default to AWS Testnet
            return 50005

    @staticmethod
    def __get_default_web3_provider(network=None):
        # Todo - mainnet config
        if network == 'mainnet':
            web3_provider = {
                "type": "http",
                "uri": "http://52.14.173.249:8101",
                "host": "52.14.173.249",
                "port": "8101"
            }
        elif network == 'testnet':
            web3_provider = {
                "type": "http",
                "uri": "http://52.14.173.249:8101",
                "host": "52.14.173.249",
                "port": "8101"
            }
        else:
            # default to AWS Testnet
            web3_provider = {
                "type": "http",
                "uri": "http://52.14.173.249:8101",
                "host": "52.14.173.249",
                "port": "8101"
            }
        return web3_provider
