from workchain_sdk.documentation.sections.section import WorkchainDocSection


class WorkchainDocSectionNode(WorkchainDocSection):
    def __init__(self, root_dir, path_to_md, config, workchain_id):
        WorkchainDocSection.__init__(self, root_dir, path_to_md,
                                     config, workchain_id)

        self.bootnode_address = None
        self.bootnode_enode = None
        self.bootnode_flag = ''

    def set_geth_bootnode_flag(self, bootnode_address):
        self.bootnode_address = bootnode_address

        self.bootnode_enode = f'{self.bootnode_address}@' \
            f'{self.config["workchain"]["bootnode"]["ip"]}:' \
            f'{self.config["workchain"]["bootnode"]["port"]}'

        self.bootnode_flag = f'--bootnodes "enode://' \
            f'{self.bootnode_enode}" '
