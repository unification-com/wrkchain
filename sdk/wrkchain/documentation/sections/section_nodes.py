from wrkchain.architectures.debian import generate_geth_cmd
from wrkchain.documentation.sections.doc_section import DocSection


class SectionNodes(DocSection):
    def __init__(self, section_number, title, nodes, wrkchain_id,
                 bootnode_config, build_dir):
        path_to_md = 'node.md'
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
            copy_static_files = ''

            if self.__bootnode_config['type'] == 'static':
                copy_static_files = \
                    self.__static_bootnode_file_copy(doc_build_dir,
                                                     public_address)

            geth_cmd = generate_geth_cmd(
                node, self.__bootnode_config, self.__wrkchain_id, listen_port,
                linebreak=True, gopath='$GOPATH', docker=False,
                path_to='~/.ethereum')

            if node['is_validator']:
                node_types.append('Validator')
            if node['rpc']:
                node_types.append('JSON RPC')

            d = {'__NODE_NUM__': str(i + 1),
                 '__EV_PUBLIC_ADDRESS__': public_address,
                 '__GETH_COMMAND__': geth_cmd,
                 '__NODE_TYPE__': ' & '.join(node_types),
                 '__NODE_TITLE__': node['title'],
                 '__COPY_STATIC_FILES__': copy_static_files,
                 '__NODE_IP__': node_ip,
                 '__BUILD_DIR__': doc_build_dir
                 }
            self.add_content(d, append=True)

        return self.get_contents()

    def __static_bootnode_file_copy(self, doc_build_dir, public_address):
        md_file = 'sub/misc/nodes_static_bootnode_file_copy.md'
        t = self.load_sub_section_template(md_file)

        contents = t.substitute(
            {'__BOOTNODE_KEY_FILE__': public_address,
             '__BUILD_DIR__': doc_build_dir})
        return contents


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
