from web3 import Web3

from wrkchain import constants
from wrkchain.documentation.sections.doc_section import DocSection


class SectionSetup(DocSection):
    def __init__(self, section_number, title, network, oracle_addresses,
                 wrkchain_id, mainchain_rpc_host, mainchain_rpc_port,
                 mainchain_rpc_uri, mainchain_network_id, genesis_json,
                 build_dir):
        path_to_md = 'setup.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__network = network
        self.__oracle_addresses = oracle_addresses
        self.__section_number = section_number
        self.__sub_section_number = 1
        self.__wrkchain_id = wrkchain_id
        self.__mainchain_rpc_host = mainchain_rpc_host
        self.__mainchain_rpc_port = mainchain_rpc_port
        self.__mainchain_rpc_uri = mainchain_rpc_uri
        self.__mainchain_network_id = mainchain_network_id
        self.__genesis_json = genesis_json
        self.__build_dir = build_dir

    def generate(self):
        d = {
            '__FUND_ORACLE_ADDRESSES__': self.__fund(),
            '__MAINCHAIN_NETWORK__': self.__network_title()
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __network_title(self):
        if self.__network == 'eth':
            network_title = 'Ethereum mainnet'
        else:
            network_title = f'UND {self.__network}'
        return network_title

    def __fund(self):
        md_file = f'sub/fund/{self.__network}.md'
        t = self.load_sub_section_template(md_file)

        if self.__network == 'testnet':
            fund_content = self.__fund_testnet(t)
        elif self.__network == 'mainnet':
            fund_content = self.__fund_mainnet(t)
        elif self.__network == 'eth':
            fund_content = self.__fund_eth(t)
        else:
            fund_content = ''

        return fund_content

    def __fund_testnet(self, t):
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses),
            '__FAUCET_URL___': constants.TESTNET_FAUCET_URL
        }
        fund_content = t.substitute(d)

        return fund_content

    def __fund_mainnet(self, t):
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses),
            '__MAINNET_UND_FUND_URL__': constants.MAINNET_UND_FUND_URL
        }
        fund_content = t.substitute(d)

        return fund_content

    def __fund_eth(self, t):
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses)
        }
        fund_content = t.substitute(d)

        return fund_content

    def __deply_contract(self):
        if self.__network == 'eth':
            deploy_content = self.__deploy_eth_mainnet()
        else:
            deploy_content = ''

        return deploy_content

    def __deploy_eth_mainnet(self):
        md_file = f'sub/deploy_wrkchain_root_contract/ethereum.md'
        t = self.load_sub_section_template(md_file)
        d = {
            '__SECTION_NUMBER__': self.__section_number,
            '__SUB_SECTION_NUMBER__': self.__sub_section_number
        }

        self.__sub_section_number += 1

        deploy_content = t.substitute(d)

        return deploy_content


class SectionSetupBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, network, oracle_addresses,
                 wrkchain_id, mainchain_rpc_host, mainchain_rpc_port,
                 mainchain_rpc_uri, mainchain_network_id, genesis_json,
                 build_dir, **_ignored):

        if not self.__instance:
            self.__instance = SectionSetup(section_number, title, network,
                                           oracle_addresses, wrkchain_id,
                                           mainchain_rpc_host,
                                           mainchain_rpc_port,
                                           mainchain_rpc_uri,
                                           mainchain_network_id,
                                           genesis_json, build_dir)
        return self.__instance
