from wrkchain.documentation.sections.doc_section import DocSection
from wrkchain.architectures.debian import generate_geth_cmd


class SectionNodes(DocSection):
    def __init__(self, section_number, title, nodes, wrkchain_id,
                 bootnode_config, build_dir):
        path_to_md = 'nodes.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__nodes = nodes
        self.__wrkchain_id = wrkchain_id
        self.__bootnode_config = bootnode_config
        self.__build_dir = build_dir

    def generate(self):

        doc_build_dir = self.__build_dir.replace('../', '')

        for i in range(len(self.__nodes)):
            node_types = []
            node = self.__nodes[i]

            public_address = node['address']
            listen_port = node['listen_port']
            node_ip = node['ip']
            copy_static_nodes_json = ''
            copy_node_key = ''

            if self.__bootnode_config['type'] == 'static':
                copy_static_nodes_json = f'2. `{doc_build_dir}/' \
                    f'static-nodes.json` to `~/.ethereum`'
                copy_node_key = f'3. `{doc_build_dir}/node_keys/' \
                    f'{public_address}.key` to `~/.ethereum/node_keys`'

            geth_cmd = generate_geth_cmd(
                node, self.__bootnode_config, self.__wrkchain_id, listen_port,
                linebreak=True, gopath='$GOPATH', docker=False,
                path_to='~/ethereum')

            if node['is_validator']:
                node_types.append('Validator')
            if node['rpc']:
                node_types.append('JSON RPC')

            d = {'__NODE_NUM__': str(i + 1),
                 '__EV_PUBLIC_ADDRESS__': public_address,
                 '__GETH_COMMAND__': geth_cmd,
                 '__NODE_TYPE__': ' & '.join(node_types),
                 '__NODE_TITLE__': node['title'],
                 '__COPY_STATIC_NODES_JSON__': copy_static_nodes_json,
                 '__NODE_IP__': node_ip,
                 '__BUILD_DIR__': doc_build_dir,
                 '__COPY_NODE_KEY__': copy_node_key
                 }
            self.add_content(d, append=True)

        return self.get_contents()


class SectionNodesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, nodes, wrkchain_id,
                 bootnode_config, build_dir, **_ignored):
        if not self.__instance:
            self.__instance = SectionNodes(section_number, title,
                                           nodes, wrkchain_id,
                                           bootnode_config, build_dir)
        return self.__instance
