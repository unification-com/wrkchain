import json
import re
from string import Template

import pypandoc

from wrkchain.documentation.sections.section import section_factory
from wrkchain.utils import repo_root


class WRKChainDocumentation:
    def __init__(self, wrkchain_name, nodes, mainchain_network,
                 ledger_base_type, oracle_addresses, mainchain_web3_provider,
                 mainchain_network_id, wrkchain_id, bootnode_config,
                 genesis_json, build_dir, oracle_write_frequency, consensus):

        self.__doc_params = {
            'wrkchain_name': wrkchain_name,
            'wrkchain_id': wrkchain_id,
            'bootnode_config': bootnode_config,
            'nodes': nodes,
            'network': mainchain_network,
            'base': ledger_base_type,
            'oracle_addresses': oracle_addresses,
            'mainchain_rpc_host': mainchain_web3_provider['host'],
            'mainchain_rpc_port': mainchain_web3_provider['port'],
            'mainchain_rpc_type': mainchain_web3_provider['type'],
            'mainchain_rpc_uri': mainchain_web3_provider['uri'],
            'mainchain_network_id': mainchain_network_id,
            'genesis_json': json.dumps(genesis_json, separators=(',', ':')),
            'build_dir': build_dir,
            'oracle_write_frequency': oracle_write_frequency,
            'consensus': consensus
        }

        # Section order is also defined here, by order of the elements in dict
        self.__documentation_sections = {
            '__SECTION_INTRODUCTION__': {
                'content': '',
                'title': 'Introduction'
            },
            '__SECTION_INSTALLATION__': {
                'content': '',
                'title': 'Installation'
            },
            '__SECTION_SETUP__': {
                'content': '',
                'title': 'Setup'
            },
            '__SECTION_BOOTNODE__': {
                'content': '',
                'title': 'Running your Bootnode'
            },
            '__SECTION_NODES__':  {
                'content': '',
                'title': 'Running your Nodes'
            },
            '__SECTION_ORACLE__': {
                'content': '',
                'title': f'Running your WRKChain Oracle on {mainchain_network}'
            },
            '__SECTION_NETWORK__': {
                'content': '',
                'title': 'Connecting to your Network'
            },
            '__SECTION_APPENDICES__': {
                'content': '',
                'title': 'Appendices'
            },
            '__SECTION_GLOSSARY__': {
                'content': '',
                'title': 'Glossary'
            }
        }

        self.__documentation = {
            'path': 'templates/docs/md/documentation.md',
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

        self.__generate_documentation()

    def get_md(self):
        return self.__documentation['content']

    def get_html(self):
        html = ''
        if self.__documentation['content']:
            root = repo_root()
            html_template_path = root / 'templates/docs/html/index.html'
            html_template = html_template_path.read_text()

            css_template_path = root / \
                'templates/docs/html/github-markdown.css'

            html_body = pypandoc.convert_text(
                self.__documentation['content'],
                'html',
                format='markdown',
                extra_args=['--section-divs']
            )
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

    def __generate_documentation(self):
        template = Template(self.__documentation['template'])
        d = {}

        for section_key, section_data in \
                self.__documentation_sections.items():
            d[section_key] = section_data['content']

        doc_title = f'"' \
            f'{self.__doc_params["wrkchain_name"]}" Documentation'
        doc_title += f'\n{"=" * len(doc_title)}\n\n' \
            f'# Contents\n'

        documentation_content = template.substitute(d)

        documentation = pypandoc.convert(
            documentation_content,
            'md', format='md',
            extra_args=['-s', '--toc', '--toc-depth=4', '--atx-headers'])

        self.__documentation['content'] = doc_title + documentation
