from wrkchain.documentation.sections.doc_section import DocSection
from wrkchain.architectures.debian import generate_geth_cmd


class SectionNodes(DocSection):
    def __init__(self, section_number, title, nodes, wrkchain_id,
                 bootnode_config):
        path_to_md = 'nodes.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__nodes = nodes
        self.__wrkchain_id = wrkchain_id
        self.__bootnode_config = bootnode_config

    def generate(self):
        for i in range(len(self.__nodes)):
            node_types = []
            node = self.__nodes[i]

            public_address = node['address']
            listen_port = node['listen_port']
            copy_static_nodes_json = ''

            if self.__bootnode_config['type'] == 'static':
                copy_static_nodes_json = 'Copy `build/static-nodes.json` to' \
                                         '`~/.ethereum`'

            geth_cmd = generate_geth_cmd(
                node, self.__bootnode_config, self.__wrkchain_id, listen_port,
                linebreak=True, gopath='$GOPATH')

            if node['is_validator']:
                node_types.append('Validator')
            else:
                node_types.append('JSON RPC')

            d = {'__NODE_NUM__': str(i + 1),
                 '__EV_PUBLIC_ADDRESS__': public_address,
                 '__GETH_COMMAND__': geth_cmd,
                 '__NODE_TYPE__': ' & '.join(node_types),
                 '__NODE_TITLE__': node['title'],
                 '__COPY_STATIC_NODES_JSON__': copy_static_nodes_json
                 }
            self.add_content(d, append=True)

        return self.get_contents()


class SectionNodesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, nodes, wrkchain_id,
                 bootnode_config, **_ignored):
        if not self.__instance:
            self.__instance = SectionNodes(section_number, title,
                                           nodes, wrkchain_id,
                                           bootnode_config)
        return self.__instance
