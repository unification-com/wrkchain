from string import Template

from workchain_sdk.documentation.sections.section import WorkchainDocSection


class WorkchainDocSectionSetup(WorkchainDocSection):
    def __init__(self, root_dir, config, workchain_id):
        path_to_md = 'sections/setup.md'

        WorkchainDocSection.__init__(self, root_dir,
                                          path_to_md, config,
                                          workchain_id)
        self.__oracle_addresses = None

    def generate(self, network, oracle_addresses):
        self.__oracle_addresses = oracle_addresses
        fund_md = f'templates/docs/md/sections/fund_{network}.md'
        fund_template_path = self.root_dir / fund_md
        fund_template = fund_template_path.read_text()
        t = Template(fund_template)

        if network == 'testnet':
            fund_content = self.__func_testnet(t)
        elif network == 'mainnet':
            fund_content = ''
        else:
            fund_content = ''

        d = {
            '__FUND_ORACLE_ADDRESSES__': fund_content
        }

        return self.generate_content(d, append=False)

    def __func_testnet(self, t):
        faucet_urls = ''
        for address in self.__oracle_addresses:
            faucet_urls += f'<http://52.14.173.249/sendtx?to={address}>  \n'
        fund_content = t.substitute({'__FAUCET_URLS___': faucet_urls})

        return fund_content
