from workchain.documentation.sections.doc_section import DocSection


class SectionRpcNodes(DocSection):
    def __init__(self, section_number, title, rpc_nodes, workchain_id,
                 bootnode_config):
        path_to_md = 'sections/rpc_nodes.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__rpc_nodes = rpc_nodes
        self.__workchain_id = workchain_id
        self.__bootnode_config = bootnode_config

    def generate(self):
        if self.__bootnode_config['type'] == 'dedicated':
            bootnode_flag = f'--bootnodes "' \
                f'{self.__bootnode_config["nodes"]["enode"]}" '
        else:
            bootnode_flag = ''

        for i in range(len(self.__rpc_nodes)):
            d = {'__NODE_NUM__': str(i + 1),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': bootnode_flag
                 }

            self.add_content(d, append=True)

        return self.get_contents()


class SectionRpcNodesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, rpc_nodes, workchain_id,
                 bootnode_config, **_ignored):

        if not self.__instance:
            self.__instance = SectionRpcNodes(section_number, title, rpc_nodes,
                                              workchain_id, bootnode_config)
        return self.__instance
