from web3 import Web3

from wrkchain import constants
from wrkchain.documentation.sections.doc_section import DocSection


class SectionSetup(DocSection):
    def __init__(self, section_number, title, network, oracle_addresses,
                 wrkchain_id, mainchain_rpc_host, mainchain_rpc_port,
                 mainchain_rpc_uri, mainchain_network_id, genesis_json):
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

    def generate(self):
        d = {
            '__FUND_ORACLE_ADDRESSES__': self.__fund(),
            '__DEPLOY_WRKCHAIN_ROOT_CONTRACT__': self.__deply_contract(),
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
        faucet_urls = ''
        for address in self.__oracle_addresses:
            faucet_urls += f'<{constants.TESTNET_FAUCET_URL}{address}>  \n'
        fund_content = t.substitute({'__FAUCET_URLS___': faucet_urls})

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
        if self.__network == 'testnet':
            deploy_content = self.__deploy_truffle()
            deploy_content += self.__deploy_oracle_deploy()
            deploy_content += self.__deploy_manual()
        elif self.__network == 'mainnet':
            deploy_content = self.__deploy_oracle_deploy()
            deploy_content += self.__deploy_manual()
        else:
            deploy_content = ''

        return deploy_content

    def __deploy_truffle(self):
        md_file = f'sub/deploy_wrkchain_root_contract/truffle.md'
        t = self.load_sub_section_template(md_file)
        genesis_sha3_bytes = \
            Web3.sha3(text=f'{self.__genesis_json.encode("utf-8")}')
        genesis_sha3 = genesis_sha3_bytes.hex()

        d = {
            '__SECTION_NUMBER__': self.__section_number,
            '__SUB_SECTION_NUMBER__': self.__sub_section_number,
            '__MAINCHAIN_RPC_HOST__': self.__mainchain_rpc_host,
            '__MAINCHAIN_RPC_PORT__': self.__mainchain_rpc_port,
            '__MAINCHAIN_NETWORK_ID__': self.__mainchain_network_id,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
            '__WRKCHAIN_GENESIS__': self.__genesis_json,
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__WRKCHAIN_EVS__': (', '.join('"' + item + '"' for item in
                                           self.__oracle_addresses)),
            '__GENESIS_SHA3__': genesis_sha3
        }

        self.__sub_section_number += 1

        deploy_content = t.substitute(d)

        return deploy_content

    def __deploy_manual(self):
        md_file = f'sub/deploy_wrkchain_root_contract/manual.md'
        t = self.load_sub_section_template(md_file)
        genesis_sha3_bytes = \
            Web3.sha3(text=f'{self.__genesis_json.encode("utf-8")}')
        genesis_sha3 = genesis_sha3_bytes.hex()

        d = {
            '__SECTION_NUMBER__': self.__section_number,
            '__SUB_SECTION_NUMBER__': self.__sub_section_number,
            '__MAINCHAIN_RPC_HOST__': self.__mainchain_rpc_host,
            '__MAINCHAIN_RPC_PORT__': self.__mainchain_rpc_port,
            '__MAINCHAIN_NETWORK_ID__': self.__mainchain_network_id,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
            '__WRKCHAIN_GENESIS__': self.__genesis_json,
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__WRKCHAIN_EVS__': (', '.join('"' + item + '"' for item in
                                           self.__oracle_addresses)),
            '__GENESIS_SHA3__': genesis_sha3
        }

        self.__sub_section_number += 1

        deploy_content = t.substitute(d)

        return deploy_content

    def __deploy_oracle_deploy(self):
        md_file = f'sub/deploy_wrkchain_root_contract/oracle_deploy.md'
        t = self.load_sub_section_template(md_file)
        genesis_sha3_bytes = \
            Web3.sha3(text=f'{self.__genesis_json.encode("utf-8")}')
        genesis_sha3 = genesis_sha3_bytes.hex()

        d = {
            '__SECTION_NUMBER__': self.__section_number,
            '__SUB_SECTION_NUMBER__': self.__sub_section_number,
            '__MAINCHAIN_NETWORK_ID__': self.__mainchain_network_id,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
            '__WRKCHAIN_GENESIS__': self.__genesis_json,
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__WRKCHAIN_EVS__': (', '.join('"' + item + '"' for item in
                                           self.__oracle_addresses)),
            '__GENESIS_SHA3__': genesis_sha3
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
                 **_ignored):

        if not self.__instance:
            self.__instance = SectionSetup(section_number, title, network,
                                           oracle_addresses, wrkchain_id,
                                           mainchain_rpc_host,
                                           mainchain_rpc_port,
                                           mainchain_rpc_uri,
                                           mainchain_network_id,
                                           genesis_json)
        return self.__instance
