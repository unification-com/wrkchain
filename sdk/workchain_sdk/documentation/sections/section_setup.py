from string import Template

from workchain_sdk.documentation.sections.doc_section import DocSection

TESTNET_FAUCET_URL = 'http://52.14.173.249/sendtx?to='


class SectionSetup(DocSection):
    def __init__(self, network, oracle_addresses):
        path_to_md = 'sections/setup.md'
        DocSection.__init__(self, path_to_md)

        self.__network = network
        self.__oracle_addresses = oracle_addresses

    def generate(self):
        fund_md = f'templates/docs/md/sections/fund_{self.__network}.md'
        fund_template_path = self.root_dir / fund_md
        fund_template = fund_template_path.read_text()
        t = Template(fund_template)

        if self.__network == 'testnet':
            fund_content = self.__func_testnet(t)
        elif self.__network == 'mainnet':
            fund_content = ''
        else:
            fund_content = ''

        d = {
            '__FUND_ORACLE_ADDRESSES__': fund_content
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __func_testnet(self, t):
        faucet_urls = ''
        for address in self.__oracle_addresses:
            faucet_urls += f'<{TESTNET_FAUCET_URL}{address}>  \n'
        fund_content = t.substitute({'__FAUCET_URLS___': faucet_urls})

        return fund_content


class SectionSetupBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, network, oracle_addresses, **_ignored):

        if not self.__instance:
            self.__instance = SectionSetup(network, oracle_addresses)
        return self.__instance
