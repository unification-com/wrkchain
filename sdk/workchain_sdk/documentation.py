from workchain_sdk.utils import repo_root


class WorkchainDocumentation:
    def __init__(self, config, workchain_id):
        self.__config = config
        self.__workchain_id = workchain_id

        self.__templates = {
            'workchain': {
                'path': 'templates/docs/workchain.md',
                'contents': None
            },
            'section_validators':  {
                'path': 'templates/docs/sections/validators.md',
                'contents': None
            },
            'section_nodes':  {
                'path': 'templates/docs/sections/nodes.md',
                'contents': None
            }
        }

        self.__load_templates()

    def generate(self):
        self.__generate_validators_section()
        self.__generate_rpc_nodes_section()
        self.__generate_documentation()
        return self.get_doc()

    def get_doc(self):
        return self.__templates['workchain']['contents']

    def __load_templates(self):
        root = repo_root()

        for key, data in self.__templates.items():
            template_path = root / data['path']
            self.__templates[key]['contents'] = template_path.read_text()

    def __generate_validators_section(self):
        template = self.__templates['section_validators']['contents']
        contents = ''

        validators = self.__config['workchain']['validators']

        val_count = 1
        for validator in validators:
            c = template
            c = c.replace('[__VALIDATOR_NUM__]', str(val_count))
            c = c.replace('[__WORKCHAIN_NETWORK_ID__]', str(self.__workchain_id))
            c = c.replace('[__BOOTNODE__]', 'abcd@123.123.123.123:30301')
            c = c.replace('[__EV_PUBLIC_ADDRESS__]', validator['address'])
            c = c.replace('[__BASE_TO_CLONE__]',
                                      'https://github.com/ethereum/go-ethereum')

            val_count = val_count + 1

            contents = contents + c

        self.__templates['section_validators']['contents'] = contents

    def __generate_rpc_nodes_section(self):
        template = self.__templates['section_nodes']['contents']
        contents = ''

        rpc_nodes = self.__config['workchain']['rpc_nodes']

        node_count = 1
        for rpc_node in rpc_nodes:
            c = template
            c = c.replace('[__NODE_NUM__]', str(node_count))
            c = c.replace('[__WORKCHAIN_NETWORK_ID__]', str(self.__workchain_id))
            c = c.replace('[__BOOTNODE__]', 'abcd@123.123.123.123:30301')
            c = c.replace('[__BASE_TO_CLONE__]',
                                      'https://github.com/ethereum/go-ethereum')

            node_count = node_count + 1

            contents = contents + c

        self.__templates['section_nodes']['contents'] = contents

    def __generate_documentation(self):
        content = self.__templates['workchain']['contents']

        content = content.replace('[__WORKCHAIN_NAME__]',
                        self.__config['workchain']['title'])
        content = content.replace('[__VALIDATORS_SECTION__]',
                        self.__templates['section_validators']['contents'])
        content = content.replace('[__JSON_RPC_NODES_SECTION__]',
                        self.__templates['section_nodes']['contents'])

        self.__templates['workchain']['contents'] = content
