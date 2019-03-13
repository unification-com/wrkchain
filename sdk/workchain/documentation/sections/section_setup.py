from string import Template

from web3 import Web3
from workchain.documentation.sections.doc_section import DocSection

TESTNET_FAUCET_URL = 'http://52.14.173.249/sendtx?to='


class SectionSetup(DocSection):
    def __init__(self, section_number, title, network, oracle_addresses,
                 workchain_id, mainchain_rpc_host, mainchain_rpc_port,
                 mainchain_rpc_uri, mainchain_network_id, genesis_json):
        path_to_md = 'sections/setup.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__network = network
        self.__oracle_addresses = oracle_addresses
        self.__section_number = section_number
        self.__workchain_id = workchain_id
        self.__mainchain_rpc_host = mainchain_rpc_host
        self.__mainchain_rpc_port = mainchain_rpc_port
        self.__mainchain_rpc_uri = mainchain_rpc_uri
        self.__mainchain_network_id = mainchain_network_id
        self.__genesis_json = genesis_json

    def generate(self):
        d = {
            '__FUND_ORACLE_ADDRESSES__': self.__fund(),
            '__DEPLOY_WORKCHAIN_ROOT_CONTRACT__': self.__deply_contract(),
            '__MAINCHAIN_NETWORK__': self.__network
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __fund(self):
        fund_md = f'templates/docs/md/sections/fund_{self.__network}.md'
        fund_template_path = self.root_dir / fund_md
        fund_template = fund_template_path.read_text()
        t = Template(fund_template)

        if self.__network == 'testnet':
            fund_content = self.__fund_testnet(t)
        elif self.__network == 'mainnet':
            fund_content = self.__fund_mainnet(t)
        else:
            fund_content = ''

        return fund_content

    def __fund_testnet(self, t):
        faucet_urls = ''
        for address in self.__oracle_addresses:
            faucet_urls += f'<{TESTNET_FAUCET_URL}{address}>  \n'
        fund_content = t.substitute({'__FAUCET_URLS___': faucet_urls})

        return fund_content

    def __fund_mainnet(self, t):
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses)
        }
        fund_content = t.substitute(d)

        return fund_content

    def __deply_contract(self):
        deploy_md = f'templates/docs/md/sections/deploy_root_contract_{self.__network}.md'
        deploy_template_path = self.root_dir / deploy_md
        deploy_template = deploy_template_path.read_text()
        t = Template(deploy_template)

        if self.__network == 'testnet':
            deploy_content = self.__deply_contract_testnet(t)
        elif self.__network == 'mainnet':
            deploy_content = ''
        else:
            deploy_content = ''

        return deploy_content

    def __deply_contract_testnet(self, t):

        genesis_sha3_bytes = \
            Web3.sha3(text=f'{self.__genesis_json.encode("utf-8")}')
        genesis_sha3 = genesis_sha3_bytes.hex()

        d = {
            '__SECTION_NUMBER__': self.__section_number,
            '__MAINCHAIN_RPC_HOST__': self.__mainchain_rpc_host,
            '__MAINCHAIN_RPC_PORT__': self.__mainchain_rpc_port,
            '__MAINCHAIN_NETWORK_ID__': self.__mainchain_network_id,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
            '__WORKCHAIN_GENESIS__': self.__genesis_json,
            '__WORKCHAIN_NETWORK_ID__': self.__workchain_id,
            '__WORKCHAIN_EVS__': (', '.join('"' + item + '"' for item in
                                            self.__oracle_addresses)),
            '__GENESIS_SHA3__': genesis_sha3
        }

        deploy_content = t.substitute(d)

        return deploy_content


class SectionSetupBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, network, oracle_addresses,
                 workchain_id, mainchain_rpc_host, mainchain_rpc_port,
                 mainchain_rpc_uri, mainchain_network_id, genesis_json,
                 **_ignored):

        if not self.__instance:
            self.__instance = SectionSetup(section_number, title, network,
                                           oracle_addresses, workchain_id,
                                           mainchain_rpc_host,
                                           mainchain_rpc_port,
                                           mainchain_rpc_uri,
                                           mainchain_network_id,
                                           genesis_json)
        return self.__instance
