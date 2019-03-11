from workchain_sdk.documentation.sections.section_node import WorkchainDocSectionNode


class WorkchainDocSectionValidators(WorkchainDocSectionNode):
    def __init__(self, root_dir, config, workchain_id):
        path_to_md = 'sections/validators.md'

        WorkchainDocSectionNode.__init__(self, root_dir, path_to_md,
                                         config, workchain_id)

    def generate(self, validators, bootnode_address=None):
        if bootnode_address:
            self.set_geth_bootnode_flag(bootnode_address)

        for i in range(len(validators)):
            d = {'__VALIDATOR_NUM__': str(i+1),
                 '__WORKCHAIN_NETWORK_ID__': str(self.workchain_id),
                 '__BOOTNODE__': self.bootnode_flag,
                 '__EV_PUBLIC_ADDRESS__': validators[i]['address']
                 }
            self.generate_content(d, append=True)

        return self.get_contents()
