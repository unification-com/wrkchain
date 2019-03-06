from web3 import Web3


class UndMainchain:
    def __init__(self, network="testnet", web3_type=None, web3_uri=None):
        self.__network = network
        self.__web3_type = web3_type
        self.__web3_uri = web3_uri

        self.__web3_provider = None
        self.__web3 = None

        self.__get_web3()

    @staticmethod
    def clean_address(address):
        return Web3.toChecksumAddress(address)

    def check_und_funds(self, address):
        und_balance = 0
        address = self.clean_address(address)

        if self.__web3.isAddress(address):
            und_balance = self.__web3.eth.getBalance(address)

        return und_balance

    def __get_web3(self):

        if self.__web3_type == 'http':
            self.__web3_provider = Web3.HTTPProvider(self.__web3_uri)
        elif self.__web3_type == 'ipc':
            self.__web3_provider = Web3.IPCProvider(self.__web3_uri)
        elif self.__web3_type == 'ws':
            self.__web3_provider = Web3.WebsocketProvider(self.__web3_uri)
        else:
            print("unknown Web3 type")

        if self.__web3_provider:
            self.__web3 = Web3(self.__web3_provider)
