from string import Template

import pypandoc

from workchain_sdk.documentation.sections.section_node_validators \
    import WorkchainDocSectionValidators
from workchain_sdk.documentation.sections.section_node_rpc_nodes \
    import WorkchainDocSectionRpcNodes
from workchain_sdk.documentation.sections.section_node_bootnode \
    import WorkchainDocSectionBootNodes
from workchain_sdk.documentation.sections.section_oracle \
    import WorkchainDocSectionOracle
from workchain_sdk.documentation.sections.section_network \
    import WorkchainDocSectionNetwork
from workchain_sdk.documentation.sections.section_installation_geth \
    import WorkchainDocSectionInstallationGeth
from workchain_sdk.documentation.sections.section_setup \
    import WorkchainDocSectionSetup
from workchain_sdk.utils import repo_root, get_oracle_addresses


class WorkchainDocumentation:
    def __init__(self, config, workchain_id, bootnode_address=None):
        self.__config = config
        self.__workchain_id = workchain_id
        self.__bootnode_address = bootnode_address

        self.__root_dir = repo_root()

        self.__documentation_sections = {
            '__SECTION_VALIDATORS__':  {
                'contents': '',
                'generate': self.__generate_validators_section
            },
            '__SECTION_JSON_RPC_NODES__':  {
                'contents': '',
                'generate': self.__generate_rpc_nodes_section
            },
            '__SECTION_BOOTNODE__':  {
                'contents': '',
                'generate': None
            },
            '__SECTION_INSTALLATION__': {
                'contents': '',
                'generate': self.__generate_installation_section
            },
            '__SECTION_ORACLE__': {
                'contents': '',
                'generate': self.__generate_oracle_section
            },
            '__SECTION_NETWORK__': {
                'contents': '',
                'generate': self.__generate_network_section
            },
            '__SECTION_SETUP__': {
                'contents': '',
                'generate': self.__generate_setup_section
            }
        }

        if bootnode_address:
            self.__documentation_sections['__SECTION_BOOTNODE__']['generate'] \
                = self.__generate_bootnode_section

        self.__documentation = {
            'path': 'templates/docs/md/README.md',
            'contents': '',
            'template': None
        }

        self.__load_template()

    def generate(self):
        for key, data in self.__documentation_sections.items():
            if data['generate']:
                data['generate'](key)

        self.__generate_readme()

    def get_md(self):
        return self.__documentation['contents']

    def get_html(self):
        html = ''
        if self.__documentation['contents']:
            root = repo_root()
            html_template_path = root / 'templates/docs/html/index.html'
            html_template = html_template_path.read_text()

            css_template_path = root / 'templates/docs/html/bare.min.css'

            html_body = pypandoc.convert_text(
                self.__documentation['contents'],
                'html', format='md')
            t = Template(html_template)

            data = {
                '__DOCUMENTATION_BODY__': html_body,
                '__CSS__': css_template_path.read_text()
            }

            html = t.substitute(data)

        return html

    def __load_template(self):
        template_path = self.__root_dir / self.__documentation['path']
        self.__documentation['template'] = \
            template_path.read_text()

    def __generate_validators_section(self, section_key):
        section_class = WorkchainDocSectionValidators(repo_root(),
                                                      self.__config,
                                                      self.__workchain_id)

        self.__documentation_sections[section_key]['contents'] \
            = section_class.generate(self.__config['workchain']['validators'],
                                     bootnode_address=self.__bootnode_address)

    def __generate_rpc_nodes_section(self, section_key):
        section_class = WorkchainDocSectionRpcNodes(repo_root(),
                                                    self.__config,
                                                    self.__workchain_id)

        self.__documentation_sections[section_key]['contents'] \
            = section_class.generate(self.__config['workchain']['rpc_nodes'],
                                     bootnode_address=self.__bootnode_address)

    def __generate_bootnode_section(self, section_key):
        section_class = WorkchainDocSectionBootNodes(repo_root(),
                                                     self.__config,
                                                     self.__workchain_id)

        self.__documentation_sections[section_key]['contents'] \
            = section_class.generate(bootnode_address=self.__bootnode_address)

    def __generate_oracle_section(self, section_key):
        section_class = WorkchainDocSectionOracle(repo_root(),
                                                  self.__config,
                                                  self.__workchain_id)

        self.__documentation_sections[section_key]['contents'] \
            = section_class.generate(get_oracle_addresses(self.__config))

    def __generate_network_section(self, section_key):
        section_class = WorkchainDocSectionNetwork(repo_root(),
                                                  self.__config,
                                                  self.__workchain_id)

        self.__documentation_sections[section_key]['contents'] \
            = section_class.generate()

    def __generate_installation_section(self, section_key):

        if self.__config["workchain"]["ledger"]["base"] == 'geth':
            class_name = WorkchainDocSectionInstallationGeth
        else:
            class_name = WorkchainDocSectionInstallationGeth

        section_class = class_name(repo_root(), self.__config,
                                   self.__workchain_id)

        self.__documentation_sections[section_key]['contents'] \
            = section_class.generate()

    def __generate_setup_section(self, section_key):
        # Load the sub section
        network = self.__config["mainchain"]["network"]
        oracle_addresses = get_oracle_addresses(self.__config)

        section_class = WorkchainDocSectionSetup(repo_root(),
                                                 self.__config,
                                                 self.__workchain_id)

        self.__documentation_sections[section_key]['contents'] \
            = section_class.generate(network, oracle_addresses)

    def __generate_readme(self):
        template = Template(self.__documentation['template'])
        d = {'__WORKCHAIN_NAME__': self.__config['workchain']['title']}

        for section_key, section_data in \
                self.__documentation_sections.items():
            d[section_key] = section_data['contents']

        self.__documentation['contents'] = template.substitute(d)
