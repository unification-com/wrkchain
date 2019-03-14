import json
import pprint


REQUIRED_WORKCHAIN_OVERRIDES = ['nodes']


class MissingConfigOverrideException(Exception):
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

    def print(self):
        pprint.sorted = lambda x, key=None: x
        pprint.pprint(self.__config)

    def print_overrides(self):
        pprint.sorted = lambda x, key=None: x
        pprint.pprint(self.__overrides)

    def __check_overrides(self, config_file):
        for k in REQUIRED_WORKCHAIN_OVERRIDES:
            if k not in self.__overrides['workchain'].keys():
                raise MissingConfigOverrideException(f'No nodes defined in '
                                                     f'{config_file}. You must'
                                                     f' define at least one '
                                                     f'node')

        if len(self.__overrides['workchain']['nodes']) == 0:
            raise MissingConfigOverrideException(f'No nodes defined in '
                                                 f'{config_file}. You must'
                                                 f' define at least one '
                                                 f'node')

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
        for node in nodes:
            new_node = self.__load_default_node()

            for key, data in node.items():
                if key == 'rpc':
                    if isinstance(data, bool):
                        # defaults already loaded
                        continue
                    else:
                        for k, d in data.items():
                            # Todo - check RPC APIs
                            new_node[key][k] = d
                else:
                    new_node[key] = data

            defined_nodes.append(new_node)

        self.__config['workchain']['nodes'] = defined_nodes

    def __override_coin(self, coin):
        if 'symbol' in coin:
            self.__config['workchain']['coin']['symbol'] = coin['symbol']
        if 'prefund' in coin:
            # Todo - check and clean input
            self.__config['workchain']['coin']['prefund'] = coin['prefund']
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
    def __load_default_node():
        node = {
            "id": "JSON-RPC Node",
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
                    "miner": False
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
        if network == 'mainchain':
            return 50000
        elif network == 'testnet':
            return 50005
        else:
            # default to AWS Testnet
            return 50005

    @staticmethod
    def __get_default_web3_provider(network=None):
        # Todo - mainnet config
        if network == 'mainchain':
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