import json
import re
from string import Template

import pypandoc

from workchain.documentation.sections.section import section_factory
from workchain.utils import repo_root


class WorkchainDocumentation:
    def __init__(self, workchain_name, nodes, mainchain_netork,
                 ledger_base_type, oracle_addresses, mainchain_web3_provider,
                 mainchain_network_id, workchain_id, bootnode_config,
                 genesis_json):

        self.__doc_params = {
            'workchain_name': workchain_name,
            'workchain_id': workchain_id,
            'bootnode_config': bootnode_config,
            'nodes': nodes,
            'network': mainchain_netork,
            'base': ledger_base_type,
            'oracle_addresses': oracle_addresses,
            'mainchain_rpc_host': mainchain_web3_provider['host'],
            'mainchain_rpc_port': mainchain_web3_provider['port'],
            'mainchain_rpc_type': mainchain_web3_provider['type'],
            'mainchain_rpc_uri': mainchain_web3_provider['uri'],
            'mainchain_network_id': mainchain_network_id,
            'genesis_json': json.dumps(genesis_json, separators=(',', ':'))
        }

        self.__documentation_sections = {
            '__SECTION_SETUP__': {
                'content': '',
                'title': 'Setup'
            },
            '__SECTION_INSTALLATION__': {
                'content': '',
                'title': 'Installation'
            },
            '__SECTION_BOOTNODE__': {
                'content': '',
                'title': 'Bootnode'
            },
            '__SECTION_NODES__':  {
                'content': '',
                'title': 'Running your Nodes'
            },
            '__SECTION_ORACLE__': {
                'content': '',
                'title': 'Running your Workchain Oracle'
            },
            '__SECTION_NETWORK__': {
                'content': '',
                'title': 'Connecting to your Network'
            },
        }

        self.__documentation = {
            'path': 'templates/docs/md/README.md',
            'content': '',
            'template': None
        }

        self.__load_template()

    def generate(self):
        section_number = 1
        for key, data in self.__documentation_sections.items():
            self.__doc_params['section_number'] = section_number
            self.__doc_params['title'] = data['title']
            section_generator = section_factory.create(key,
                                                       **self.__doc_params)
            section_contents = section_generator.generate()
            if len(section_contents) > 0:
                self.__documentation_sections[key]['content'] = \
                    section_contents
                section_number += 1

        self.__generate_readme()

    def get_md(self):
        return self.__documentation['content']

    def get_html(self):
        html = ''
        if self.__documentation['content']:
            root = repo_root()
            html_template_path = root / 'sdk' / 'templates/docs/html/index.html'
            html_template = html_template_path.read_text()

            css_template_path = root / 'sdk' / 'templates/docs/html/bare.min.css'

            html_body = pypandoc.convert_text(
                self.__documentation['content'],
                'html', format='md')
            t = Template(html_template)

            data = {
                '__DOCUMENTATION_BODY__': html_body,
                '__CSS__': css_template_path.read_text()
            }

            html = t.substitute(data)

        return html

    def __load_template(self):
        template_path = repo_root() / 'sdk' / self.__documentation['path']
        self.__documentation['template'] = \
            template_path.read_text()

    def __generate_readme(self):
        template = Template(self.__documentation['template'])
        d = {}

        for section_key, section_data in \
                self.__documentation_sections.items():
            d[section_key] = section_data['content']

        d['__CONTENTS__'] = self.__generate_contents(d)
        d['__DOCUMENTATION_TITLE__'] = f'# "' \
            f'{self.__doc_params["workchain_name"]}" Documentation'

        self.__documentation['content'] = template.substitute(d)

    @staticmethod
    def __generate_contents(d):
        header_regex = \
            re.compile(r'(^|\n)(?P<level>#{1,6})(?P<header>.*?)#*(\n|$)')

        uri_regex = re.compile('([^-\s\w]|_)+')

        contents = ''
        for section_key, section_content in d.items():
            section_titles = header_regex.findall(section_content)
            for section_title in section_titles:
                leading_spaces = ''
                if section_title[1] == '###':
                    leading_spaces = '  '
                elif section_title[1] == '####':
                    leading_spaces = '    '

                title_words = section_title[2].lstrip().split(' ')
                section_number = title_words.pop(0)  # get rid of leading #.#
                title = ' '.join(title_words)
                uri = '-'.join(
                    [uri_regex.sub('', word) for word in title_words]).lower()
                contents += f'{leading_spaces}{section_number} [{title}]' \
                    f'(#{uri})  \n'

        return contents
