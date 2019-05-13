import json
import pprint

from random import SystemRandom

from IPy import IP
from web3 import Web3

from wrkchain.utils import dict_key_exists

REQUIRED_OVERRIDES = ['wrkchain', 'mainchain']
REQUIRED_WRKCHAIN_OVERRIDES = ['nodes']
REQUIRED_WRKCHAIN_NODE_OVERRIDES = ['address', 'ip']
REQUIRED_MAINCHAIN_OVERRIDES = ['network']
VALID_MAINCHAIN_NETWORKS = ['testnet', 'mainnet', 'eth']
VALID_RPC_APIS = ['admin', 'db', 'debug', 'eth', 'miner', 'net', 'personal',
                  'shh', 'txpool', 'web3']
VALID_ORACLE_HASHES = ['parent', 'receipt', 'tx', 'state']
VALID_LEDGERS = ['geth']
VALID_GETH_CONSENSUS = ['clique']

GETH_START_PORT = 30304
RPC_START_PORT = 8545


class MissingConfigOverrideException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InvalidOverrideException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class WRKChainConfig:
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

    @staticmethod
    def generate_wrkchain_id():
        sys_random = SystemRandom()
        return sys_random.randint(99999, 9999999999)

    def __check_overrides(self, config_file):

        for k in REQUIRED_OVERRIDES:
            if k not in self.__overrides.keys():
                err = f'"{k}" not defined in {config_file}. Must ' \
                    f'define {", ".join(REQUIRED_OVERRIDES)}'

                raise MissingConfigOverrideException(err)

        for k in REQUIRED_WRKCHAIN_OVERRIDES:
            if k not in self.__overrides['wrkchain'].keys():
                err = f'"{k}" not defined in {config_file}.'
                raise MissingConfigOverrideException(err)

        if len(self.__overrides['wrkchain']['nodes']) == 0:
            err = f'No nodes defined in {config_file}. You must define ' \
                f'at least one node'
            raise MissingConfigOverrideException(err)

        for i in range(len(self.__overrides['wrkchain']['nodes'])):
            node_override = self.__overrides['wrkchain']['nodes'][i]
            for k in REQUIRED_WRKCHAIN_NODE_OVERRIDES:
                if k not in node_override.keys():
                    err = f'"{k}" not defined in wrkchain -> nodes -> Node ' \
                        f'{i} section in {config_file}.'
                    raise MissingConfigOverrideException(err)

            # Check if node has been defined as both validator and RPC node
            if dict_key_exists(node_override, 'is_validator') and \
                dict_key_exists(node_override, 'rpc'):
                if node_override['is_validator'] and node_override['rpc']:
                    node_title = ''
                    if dict_key_exists(node_override, 'title'):
                        node_title = f' ({node_override["title"]})'
                    err = f'wrkchain -> nodes -> Node {i}{node_title} Node' \
                        f' may only be defined as either Validator OR JSON ' \
                        f'RPC node'
                    raise InvalidOverrideException(err)

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

        if dict_key_exists(self.__overrides,
                           'wrkchain', 'wrkchain_network_id'):
            wrkchain_network_id = \
                self.__overrides['wrkchain']['wrkchain_network_id']
            if not isinstance(wrkchain_network_id, int):
                err = f'wrkchain_network_id "{wrkchain_network_id}" - ' \
                    f'must be an integer. Found string, or int passed ' \
                    f'as string'
                raise InvalidOverrideException(err)

        if dict_key_exists(self.__overrides,
                           'wrkchain', 'oracle_write_frequency'):
            oracle_write_frequency = \
                self.__overrides['wrkchain']['oracle_write_frequency']
            if not isinstance(oracle_write_frequency, int):
                err = f'oracle_write_frequency "{oracle_write_frequency}" - ' \
                    f'must be an integer. Found string, or int passed ' \
                    f'as string'
                raise InvalidOverrideException(err)

        if dict_key_exists(self.__overrides, 'docker_network', 'subnet'):
            subnet = self.__overrides['docker_network']['subnet']
            try:
                docker_subnet = IP(subnet)
                if len(docker_subnet) <= 1:
                    err = f'Docker subnet error ({subnet}): ' \
                        f'must be IP range, e.g. {subnet}/24'
                    raise InvalidOverrideException(err)

            except ValueError as e:
                err = f'Docker subnet error ({subnet}): {e}'
                raise InvalidOverrideException(err)

        if dict_key_exists(self.__overrides, 'wrkchain', 'ledger', 'consensus',
                           'type'):
            consensus = \
                self.__overrides['wrkchain']['ledger']['consensus']['type']
            if consensus not in VALID_GETH_CONSENSUS:
                err = f'Invalid consensus method "{consensus}"'
                raise InvalidOverrideException(err)

        if dict_key_exists(self.__overrides, 'wrkchain', 'oracle_hashes'):
            oracle_hashes = self.__overrides['wrkchain']['oracle_hashes']
            oracle_hashes_list = oracle_hashes.split(",")
            for oh in oracle_hashes_list:
                if oh not in VALID_ORACLE_HASHES:
                    err = f'Invalid Oracle hash type ({oh})'
                    raise InvalidOverrideException(err)


    def __load_basic_defaults(self):
        basic_default = {
            'wrkchain': {
                'title': 'My WRKChain',
                'oracle_write_frequency': 3600,
                'oracle_hashes': 'parent,receipt,tx,state',
                'wrkchain_network_id': False,
                'ledger': self.__load_default_ledger(),
                'bootnode': self.__load_default_bootnode(),
                'chaintest': self.__load_default_chaintest(),
                'nodes': [],
                'coin': self.__load_default_coin()
            },
            'mainchain': self.__load_default_mainchain(),
            'docker_network': self.__load_default_docker_network()
        }

        self.__config = basic_default

    def __load_overrides(self):
        wrkchain_overrides = self.__overrides['wrkchain']

        # Title
        if 'title' in wrkchain_overrides:
            self.__config['wrkchain']['title'] = wrkchain_overrides['title']

        # Oracle config
        if 'oracle_hashes' in wrkchain_overrides:
            self.__config['wrkchain']['oracle_hashes'] = \
                wrkchain_overrides['oracle_hashes']

        if 'oracle_write_frequency' in wrkchain_overrides:
            self.__config['wrkchain']['oracle_write_frequency'] = \
                wrkchain_overrides['oracle_write_frequency']

        # WRKChain Network ID
        if 'wrkchain_network_id' in wrkchain_overrides:
            wrkchain_network_id = wrkchain_overrides['wrkchain_network_id']
            if not wrkchain_network_id:
                self.__config['wrkchain']['wrkchain_network_id'] = \
                    self.generate_wrkchain_id()
            else:
                self.__config['wrkchain']['wrkchain_network_id'] = \
                    wrkchain_network_id
        else:
            self.__config['wrkchain']['wrkchain_network_id'] = \
                self.generate_wrkchain_id()

        # Docker subnet
        if 'docker_network' in self.__overrides:
            docker_network_overrides = self.__overrides['docker_network']
            self.__override_docker_network(docker_network_overrides)

        # Ledger
        if 'ledger' in wrkchain_overrides:
            self.__override_ledger(wrkchain_overrides['ledger'])

        # Bootnode
        if 'bootnode' in wrkchain_overrides:
            self.__override_bootnode(wrkchain_overrides['bootnode'])

        # Chaintest
        if 'chaintest' in wrkchain_overrides:
            self.__override_chaintest(wrkchain_overrides['chaintest'])

        # Nodes
        if 'nodes' in wrkchain_overrides:
            self.__override_nodes(wrkchain_overrides['nodes'])

        # Coin
        if 'coin' in wrkchain_overrides:
            self.__override_coin(wrkchain_overrides['coin'])

        # Mainchain
        if 'mainchain' in self.__overrides:
            mainchain_overrides = self.__overrides['mainchain']
            self.__override_mainchain(mainchain_overrides)

    def __override_ledger(self, ledger):
        # Todo - load according to selected base (geth, etc.)
        new_conf = self.__load_default_ledger()
        for key, data in ledger.items():
            new_conf[key] = data
        self.__config['wrkchain']['ledger'] = new_conf

    def __override_bootnode(self, bootnode_conf):

        new_conf = self.__load_default_bootnode()

        for key, data in bootnode_conf.items():
            if key == 'ip':
                try:
                    IP(data)
                except ValueError as e:
                    err = f'Config wrkchain.bootnode.ip error {data} ' \
                        f'is not a valid IP: {e}'
                    raise InvalidOverrideException(err)

            new_conf[key] = data
        self.__config['wrkchain']['bootnode'] = new_conf

    def __override_nodes(self, nodes):
        defined_nodes = []
        node_num = 1
        for node in nodes:
            new_node = self.__load_default_node(node_num)
            for key, data in node.items():
                new_node[key] = self.__handle_node_override(key, data,
                                                            node_num)
            node_num += 1
            defined_nodes.append(new_node)
        self.__config['wrkchain']['nodes'] = defined_nodes

    def __handle_node_override(self, key, data, node_num):
        if key == 'rpc':
            new_node_data = self.__handle_rpc_node_overrides(data, node_num)
        elif key == 'address':
            if not Web3.isAddress(data):
                err = f'wrkchain -> nodes -> {node_num - 1} -> ' \
                    f'address "{data}"" is not a valid address'
                raise InvalidOverrideException(err)
            new_node_data = Web3.toChecksumAddress(data)
        elif key == 'ip' or key == 'docker_ip':
            try:
                IP(data)
            except ValueError as e:
                err = f'Config wrkchain.nodes[{node_num - 1}].ip ' \
                    f'error {data} is not a valid IP: {e}'
                raise InvalidOverrideException(err)
            new_node_data = data
        else:
            new_node_data = data
        return new_node_data

    def __handle_rpc_node_overrides(self, data, node_num):
        new_node_data = self.__load_default_node(node_num, rpc_only=True)
        if isinstance(data, bool):
            if not data:
                new_node_data = False
        else:
            for k, d in data.items():
                if k == 'apis':
                    apis = {}
                    for api in VALID_RPC_APIS:
                        if api in data[k]:
                            apis[api] = data[k][api]
                        else:
                            apis[api] = False
                    new_node_data[k] = apis
                else:
                    new_node_data[k] = d
        return new_node_data

    def __override_coin(self, coin):
        if 'symbol' in coin:
            self.__config['wrkchain']['coin']['symbol'] = coin['symbol']
        if 'prefund' in coin:
            prefund = []
            for account in self.__overrides['wrkchain']['coin']['prefund']:
                if not Web3.isAddress(account['address']):
                    err = f'coin -> prefund -> {account["address"]} is not ' \
                        f'a valid address'
                    raise InvalidOverrideException(err)

                prefund_account = {
                    'address': Web3.toChecksumAddress(account["address"]),
                    'balance': account["balance"]
                }
                prefund.append(prefund_account)

            self.__config['wrkchain']['coin']['prefund'] = prefund
        else:
            # use address from nodes
            prefund_accounts = []
            for node in self.__config['wrkchain']['nodes']:
                account = {
                    'address': node['address'],
                    'balance': "1000000000"
                }
                prefund_accounts.append(account)
            self.__config['wrkchain']['coin']['prefund'] = prefund_accounts

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

    def __override_docker_network(self, docker_network):
        for k, v in docker_network.items():
            self.__config['docker_network'][k] = v

    def __override_chaintest(self, chaintest):
        if not isinstance(chaintest, bool):
            for k, v in chaintest.items():
                if k == 'ip':
                    try:
                        IP(v)
                    except ValueError as e:
                        err = f'Config wrkchain.chaintest.ip ' \
                            f'error {v} is not a valid IP: {e}'
                        raise InvalidOverrideException(err)
                self.__config['wrkchain']['chaintest'][k] = v

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

    def __load_default_bootnode(self):

        subnet = self.__get_docker_subnet()

        bootnode = {
            "use": False,
            "ip": subnet[2].strNormal(),
            "docker_ip": subnet[2].strNormal(),
            "port": GETH_START_PORT,
            "docker_port": GETH_START_PORT,
            "name": "wrkchain-bootnode"
        }

        return bootnode

    def __load_default_node(self, node_num, rpc_only=False):

        subnet = self.__get_docker_subnet()

        node = {
            "title": f'Validator & JSON RPC {node_num}',
            "name": f'wrkchain-node-{node_num}',
            "address": "",
            "private_key": "",
            "ip": subnet[node_num + 2].strNormal(),
            "docker_ip": subnet[node_num + 2].strNormal(),
            "listen_port": GETH_START_PORT + node_num,
            "docker_listen_port": GETH_START_PORT + node_num,
            "is_validator": True,
            "write_to_oracle": True,
            "rpc": False
        }

        rpc = {
                "port": RPC_START_PORT + (node_num - 1),
                "docker_port": RPC_START_PORT + (node_num - 1),
                "rpccorsdomain": "*",
                "rpcvhosts": "*",
                "rpcaddr": "0.0.0.0",
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

        if rpc_only:
            return rpc
        else:
            return node

    @staticmethod
    def __load_default_coin():
        coin = {
            "symbol": "WRK",
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
        elif network == 'eth':
            return 1
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
        elif network == 'eth':
            web3_provider = {
                "type": "http",
                "uri": "https://mainnet.infura.io/API_KEY",
                "host": "mainnet.infura.io",
                "port": "443"
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

    @staticmethod
    def __load_default_docker_network():
        docker_network = {
            "subnet": "172.25.0.0/24"
        }

        return docker_network

    def __get_docker_subnet(self):
        if 'docker_config' in self.__config:
            subnet = IP(self.__config['docker_network']['subnet'])
        else:
            docker_config = self.__load_default_docker_network()
            subnet = IP(docker_config['subnet'])
        return subnet

    def __load_default_chaintest(self):
        subnet = self.__get_docker_subnet()
        chaintest = {
            'use': False,
            'ip': subnet[len(subnet) - 1].strNormal()
        }
        return chaintest
