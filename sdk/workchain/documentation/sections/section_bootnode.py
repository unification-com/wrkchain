from workchain.documentation.sections.doc_section import DocSection
from workchain.documentation.sections.section_utils import SectionUtils


class SectionBootNodes(DocSection):
    def __init__(self, bootnode_address=None, bootnode_port=None,
                 bootnode_ip=None):
        path_to_md = 'sections/bootnode.md'
        DocSection.__init__(self, path_to_md)

        self.__bootnode_address = bootnode_address
        self.__bootnode_port = bootnode_port
        self.__bootnode_ip = bootnode_ip

    def generate(self):
        if self.__bootnode_address:
            bootnode_enode, bootnode_flag = SectionUtils.set_geth_bootnode_flag(
                self.__bootnode_address, self.__bootnode_ip,
                self.__bootnode_port)

            d = {'__BOOTNODE_ENODE': bootnode_enode,
                 '__BOOTNODE_PORT': self.__bootnode_port
                 }

            self.add_content(d, append=False)
            return self.get_contents()
        else:
            return ''


class SectionBootNodesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, bootnode_address=None, bootnode_port=None,
                 bootnode_ip=None, **_ignored):

        if not self.__instance:
            self.__instance = SectionBootNodes(bootnode_address,
                                               bootnode_port, bootnode_ip)
        return self.__instance
