import markdown

from workchain_sdk.utils import repo_root, get_oracle_addresses
from string import Template


class WorkchainDocumentation:
    def __init__(self, config, workchain_id, bootnode_address=None):
        self.__config = config
        self.__workchain_id = workchain_id
        self.__bootnode_address = bootnode_address

        if bootnode_address:
            self.__bootnode_enode = f'{self.__bootnode_address}@' \
                f'{self.__config["workchain"]["bootnode"]["ip"]}:' \
                f'{self.__config["workchain"]["bootnode"]["port"]}'
            self.__bootnode_flag = f'--bootnodes "enode://' \
                f'{self.__bootnode_enode}" '
        else:
            self.__bootnode_enode = None
            self.__bootnode_flag = ''

        install_md = f'install_{self.__config["workchain"]["ledger"]["base"]}'

        self.__documentation = {
            'readme': {
                'path': 'templates/docs/md/README.md',
                'contents': '',
                'template': None
            },
            'sections': {
                '__SECTION_VALIDATORS__':  {
                    'path': 'templates/docs/md/sections/validators.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_validators_section
                },
                '__SECTION_JSON_RPC_NODES__':  {
                    'path': 'templates/docs/md/sections/nodes.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_rpc_nodes_section
                },
                '__SECTION_BOOTNODE__':  {
                    'path': 'templates/docs/md/sections/bootnode.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_bootnode_section
                },
                '__SECTION_INSTALLATION__': {
                    'path': f'templates/docs/md/sections/{install_md}.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_installation_section
                },
                '__SECTION_ORACLE__': {
                    'path': 'templates/docs/md/sections/oracle.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_oracle_section
                },
                '__SECTION_NETWORK__': {
                    'path': 'templates/docs/md/sections/network.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_network_section
                },
                '__SECTION_SETUP__': {
                    'path': 'templates/docs/md/sections/setup.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_setup_section
                }
            }
        }

        self.__load_templates()

    def generate(self):
        for key, data in self.__documentation['sections'].items():
            data['generate'](key)

        self.__generate_readme()

    def get_md(self):
        return self.__documentation['readme']['contents']

    def get_html(self):
        html = ''
        if self.__documentation['readme']['contents']:
            root = repo_root()
            html_template_path = root / 'templates/docs/html/index.html'
            html_template = html_template_path.read_text()

            css_template_path = root / 'templates/docs/html/bare.min.css'

            html_body = markdown.markdown(
                self.__documentation['readme']['contents'])
            t = Template(html_template)

            data = {
                '__DOCUMENTATION_BODY__': html_body,
                '__CSS__': css_template_path.read_text()
            }

            html = t.substitute(data)

        return html

    def __load_templates(self):
        root = repo_root()

        for key, data in self.__documentation.items():
            if key == 'readme':
                template_path = root / data['path']
                self.__documentation[key]['template'] = \
                    template_path.read_text()
            else:
                for section_key, section_data in data.items():
                    template_path = root / section_data['path']
                    self.__documentation[key][section_key][
                        'template'] = template_path.read_text()

    def __generate_validators_section(self, section_name):
        validators = self.__config['workchain']['validators']

        for i in range(len(validators)):
            d = {'__VALIDATOR_NUM__': str(i+1),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': self.__bootnode_flag,
                 '__EV_PUBLIC_ADDRESS__': validators[i]['address']
                 }

            self.__generate_section(section_name, d)

    def __generate_rpc_nodes_section(self, section_name):
        rpc_nodes = self.__config['workchain']['rpc_nodes']

        for i in range(len(rpc_nodes)):
            d = {'__NODE_NUM__': str(i+1),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': self.__bootnode_flag
                 }

            self.__generate_section(section_name, d)

    def __generate_bootnode_section(self, section_name):
        if self.__bootnode_enode:
            d = {'__BOOTNODE_ENODE': self.__bootnode_enode,
                 '__BOOTNODE_PORT':
                     self.__config["workchain"]["bootnode"]["port"]
                 }

            self.__generate_section(section_name, d)

    def __generate_oracle_section(self, section_name):
        oracle_addresses = get_oracle_addresses(self.__config)
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(oracle_addresses)
        }
        self.__generate_section(section_name, d)

    def __generate_network_section(self, section_name):
        self.__generate_section(section_name, {})

    def __generate_installation_section(self, section_name):
        self.__generate_section(section_name, {})

    def __generate_setup_section(self, section_name):
        # Load the sub section
        network = self.__config["mainchain"]["network"]
        fund_md = f'templates/docs/md/sections/fund_{network}.md'
        fund_template_path = repo_root() / fund_md
        fund_template = fund_template_path.read_text()
        t = Template(fund_template)

        oracle_addresses = get_oracle_addresses(self.__config)

        if network == 'testnet':
            faucet_urls = ''
            for address in oracle_addresses:
                faucet_urls += f'<http://52.14.173.249/sendtx?to={address}>  \n'
            fund_content = t.substitute({'__FAUCET_URLS___': faucet_urls})
        elif network == 'mainnet':
            fund_content = ''
        else:
            fund_content = ''

        d = {
            '__FUND_ORACLE_ADDRESSES__': fund_content
        }
        self.__generate_section(section_name, d)

    def __generate_section(self, section, data, append=True):
        t = Template(self.__documentation['sections'][section]['template'])
        content = t.substitute(data)
        if append:
            self.__append_contents(section, content)
        else:
            return content

    def __append_contents(self, section, contents):
        self.__documentation['sections'][section]['contents'] += contents

    def __generate_readme(self):
        template = Template(self.__documentation['readme']['template'])
        d = {'__WORKCHAIN_NAME__': self.__config['workchain']['title']}

        for section_key, section_data in \
                self.__documentation['sections'].items():
            d[section_key] = section_data['contents']

        self.__documentation['readme']['contents'] = template.substitute(d)
