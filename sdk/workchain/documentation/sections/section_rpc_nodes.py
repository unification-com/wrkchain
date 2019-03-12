from workchain.documentation.sections.doc_section import DocSection
from workchain.documentation.sections.section_utils import SectionUtils


class SectionRpcNodes(DocSection):
    def __init__(self, section_number, title, rpc_nodes, workchain_id,
                 bootnode_address=None, bootnode_ip=None, bootnode_port=None):
        path_to_md = 'sections/rpc_nodes.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__rpc_nodes = rpc_nodes
        self.__workchain_id = workchain_id
        self.__bootnode_address = bootnode_address
        self.__bootnode_ip = bootnode_ip
        self.__bootnode_port = bootnode_port

    def generate(self):
        if self.__bootnode_address:
            bootnode_enode, bootnode_flag = SectionUtils.set_geth_bootnode_flag(
                self.__bootnode_address, self.__bootnode_ip,
                self.__bootnode_port)
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
                 bootnode_address=None, bootnode_ip=None, bootnode_port=None,
                 **_ignored):

        if not self.__instance:
            self.__instance = SectionRpcNodes(section_number, title, rpc_nodes,
                                              workchain_id, bootnode_address,
                                              bootnode_ip, bootnode_port)
        return self.__instance
