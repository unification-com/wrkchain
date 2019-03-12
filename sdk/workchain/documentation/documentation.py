import re
from string import Template

import pypandoc
from workchain.documentation.sections.section import factory
from workchain.utils import repo_root, get_oracle_addresses


class WorkchainDocumentation:
    def __init__(self, config, workchain_id, bootnode_address=None):
        self.__doc_params = {
            'workchain_name': config['workchain']['title'],
            'workchain_id': workchain_id,
            'bootnode_address': bootnode_address,
            'validators': config['workchain']['validators'],
            'rpc_nodes':  config['workchain']['rpc_nodes'],
            'network': config["mainchain"]["network"],
            'base': config["workchain"]["ledger"]["base"],
            'oracle_addresses': get_oracle_addresses(config)
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
            '__SECTION_VALIDATORS__':  {
                'content': '',
                'title': 'Running your Validators'
            },
            '__SECTION_JSON_RPC_NODES__':  {
                'content': '',
                'title': 'Running your JSON RPC Nodes'
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
            section_generator = factory.create(key, **self.__doc_params)
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
            html_template_path = root / 'templates/docs/html/index.html'
            html_template = html_template_path.read_text()

            css_template_path = root / 'templates/docs/html/bare.min.css'

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
        template_path = repo_root() / self.__documentation['path']
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

    def __generate_contents(self, d):
        header_regex = re.compile(r'(^|\n)(?P<level>#{1,6})(?P<header>.*?)#*(\n|$)')
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
                uri = '-'.join(title_words).lower()
                contents += f'{leading_spaces}{section_number} [{title}]' \
                    f'(#{uri})  \n'

        return contents

