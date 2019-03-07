from workchain_sdk.utils import repo_root
from string import Template


class WorkchainDocumentation:
    def __init__(self, config, workchain_id):
        self.__config = config
        self.__workchain_id = workchain_id

        self.__templates = {
            'readme': {
                'path': 'templates/docs/README.md',
                'contents': '',
                'template': None
            },
            'sections': {
                '__SECTION_VALIDATORS__':  {
                    'path': 'templates/docs/sections/validators.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_validators_section
                },
                '__SECTION_JSON_RPC_NODES__':  {
                    'path': 'templates/docs/sections/nodes.md',
                    'contents': '',
                    'template': None,
                    'generate': self.__generate_rpc_nodes_section
                }
            }
        }

        self.__load_templates()

    def generate(self):
        for key, data in self.__templates['sections'].items():
            data['generate'](key)

        self.__generate_readme()
        return self.get_doc()

    def get_doc(self):
        return self.__templates['readme']['contents']

    def __load_templates(self):
        root = repo_root()

        for key, data in self.__templates.items():
            if key == 'readme':
                template_path = root / data['path']
                self.__templates[key]['template'] = template_path.read_text()
            else:
                for section_key, section_data in data.items():
                    template_path = root / section_data['path']
                    self.__templates[key][section_key][
                        'template'] = template_path.read_text()

    def __generate_validators_section(self, section_name):
        bootnode = 'abcd@123.123.123.123:30301'
        base_clone = 'https://github.com/ethereum/go-ethereum'

        validators = self.__config['workchain']['validators']

        for i in range(len(validators)):
            d = {'__VALIDATOR_NUM__': str(i),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': bootnode,
                 '__EV_PUBLIC_ADDRESS__': validators[i]['address'],
                 '__BASE_TO_CLONE__': base_clone}

            self.__generate_section(section_name, d)

    def __generate_rpc_nodes_section(self, section_name):
        bootnode = 'abcd@123.123.123.123:30301'
        base_clone = 'https://github.com/ethereum/go-ethereum'

        rpc_nodes = self.__config['workchain']['rpc_nodes']

        for i in range(len(rpc_nodes)):
            d = {'__NODE_NUM__': str(i),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': bootnode,
                 '__BASE_TO_CLONE__': base_clone}

            self.__generate_section(section_name, d)

    def __generate_section(self, section, data, append=True):
        t = Template(self.__templates['sections'][section]['template'])
        content = t.substitute(data)
        if append:
            self.__append_contents(section, content)
        else:
            return content

    def __append_contents(self, section, contents):
        self.__templates['sections'][section]['contents'] += contents

    def __generate_readme(self):
        template = Template(self.__templates['readme']['template'])
        d = {'__WORKCHAIN_NAME__': self.__config['workchain']['title']}

        for section_key, section_data in self.__templates['sections'].items():
            d[section_key] = section_data['contents']

        self.__templates['readme']['contents'] = template.substitute(d)
