from string import Template

import pypandoc
from workchain_sdk.documentation.sections.section import factory
from workchain_sdk.utils import repo_root, get_oracle_addresses


class WorkchainDocumentation:
    def __init__(self, config, workchain_id, bootnode_address=None):
        self.__doc_params = {
            'title': config['workchain']['title'],
            'workchain_id': workchain_id,
            'bootnode_address': bootnode_address,
            'validators': config['workchain']['validators'],
            'rpc_nodes':  config['workchain']['rpc_nodes'],
            'network': config["mainchain"]["network"],
            'base': config["workchain"]["ledger"]["base"],
            'oracle_addresses': get_oracle_addresses(config)
        }

        self.__documentation_sections = {
            '__SECTION_VALIDATORS__':  '',
            '__SECTION_JSON_RPC_NODES__':  '',
            '__SECTION_BOOTNODE__': '',
            '__SECTION_INSTALLATION__': '',
            '__SECTION_ORACLE__': '',
            '__SECTION_NETWORK__': '',
            '__SECTION_SETUP__': ''
        }

        self.__documentation = {
            'path': 'templates/docs/md/README.md',
            'contents': '',
            'template': None
        }

        self.__load_template()

    def generate(self):
        for key, data in self.__documentation_sections.items():
            print(key)
            section_generator = factory.create(key, **self.__doc_params)
            print(section_generator)
            self.__documentation_sections[key] = section_generator.generate()

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
        template_path = repo_root() / self.__documentation['path']
        self.__documentation['template'] = \
            template_path.read_text()

    def __generate_readme(self):
        template = Template(self.__documentation['template'])
        d = {'__WORKCHAIN_NAME__': self.__doc_params['title']}

        for section_key, section_data in \
                self.__documentation_sections.items():
            d[section_key] = section_data

        self.__documentation['contents'] = template.substitute(d)
