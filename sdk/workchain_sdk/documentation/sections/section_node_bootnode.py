from workchain_sdk.documentation.sections.section_node import WorkchainDocSectionNode


class WorkchainDocSectionBootNodes(WorkchainDocSectionNode):
    def __init__(self, root_dir, config, workchain_id):
        path_to_md = 'sections/bootnode.md'

        WorkchainDocSectionNode.__init__(self, root_dir, path_to_md,
                                         config, workchain_id)

    def generate(self, bootnode_address=None):
        if bootnode_address:
            self.set_geth_bootnode_flag(bootnode_address)

            d = {'__BOOTNODE_ENODE': self.bootnode_enode,
                 '__BOOTNODE_PORT':
                     self.config["workchain"]["bootnode"]["port"]
                 }

            return self.generate_content(d, append=False)
        else:
            return ''
