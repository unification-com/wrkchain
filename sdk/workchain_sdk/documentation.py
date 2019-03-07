from workchain_sdk.utils import repo_root
from string import Template


class WorkchainDocumentation:
    def __init__(self, config, workchain_id):
        self.__config = config
        self.__workchain_id = workchain_id

        self.__templates = {
            'readme': {
                'path': 'templates/docs/README.md',
                'contents': None
            },
            'sections': {
                '__SECTION_VALIDATORS__':  {
                    'path': 'templates/docs/sections/validators.md',
                    'contents': None,
                },
                '__SECTION_JSON_RPC_NODES__':  {
                    'path': 'templates/docs/sections/nodes.md',
                    'contents': None
                }
            }
        }

        self.__load_templates()

    def generate(self):
        self.__generate_validators_section()
        self.__generate_rpc_nodes_section()
        self.__generate_documentation()
        return self.get_doc()

    def get_doc(self):
        return self.__templates['readme']['contents']

    def __load_templates(self):
        root = repo_root()

        for key, data in self.__templates.items():
            if key == 'readme':
                template_path = root / data['path']
                self.__templates[key]['contents'] = template_path.read_text()
            else:
                for section_key, section_data in data.items():
                    template_path = root / section_data['path']
                    self.__templates[key][section_key][
                        'contents'] = template_path.read_text()

    def __generate_validators_section(self):
        bootnode = 'abcd@123.123.123.123:30301'
        base_clone = 'https://github.com/ethereum/go-ethereum'
        contents = ''

        validators = self.__config['workchain']['validators']

        val_count = 1
        for validator in validators:
            t = self.__get_section_template('__SECTION_VALIDATORS__')
            d = {'__VALIDATOR_NUM__': str(val_count),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': bootnode,
                 '__EV_PUBLIC_ADDRESS__': validator['address'],
                 '__BASE_TO_CLONE__': base_clone}

            contents = contents + t.substitute(d)
            val_count = val_count + 1

        self.__set_section_template('__SECTION_VALIDATORS__', contents)

    def __generate_rpc_nodes_section(self):
        bootnode = 'abcd@123.123.123.123:30301'
        base_clone = 'https://github.com/ethereum/go-ethereum'
        contents = ''

        rpc_nodes = self.__config['workchain']['rpc_nodes']

        node_count = 1
        for rpc_node in rpc_nodes:
            t = self.__get_section_template('__SECTION_JSON_RPC_NODES__')
            d = {'__NODE_NUM__': str(node_count),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': bootnode,
                 '__BASE_TO_CLONE__': base_clone}

            contents = contents + t.substitute(d)

            node_count = node_count + 1

        self.__set_section_template('__SECTION_JSON_RPC_NODES__', contents)

    def __get_section_template(self, section):
        t = Template(self.__templates['sections'][section]['contents'])
        return t

    def __set_section_template(self, section, contents):
        self.__templates['sections'][section]['contents'] = contents

    def __generate_documentation(self):
        template = Template(self.__templates['readme']['contents'])
        d = {'__WORKCHAIN_NAME__': self.__config['workchain']['title']}

        for section_key, section_data in self.__templates['sections'].items():
            d[section_key] = section_data['contents']

        self.__templates['readme']['contents'] = template.substitute(d)
