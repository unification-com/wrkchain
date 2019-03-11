from workchain_sdk.documentation.sections.section import WorkchainDocSection


class WorkchainDocSectionNetwork(WorkchainDocSection):
    def __init__(self, root_dir, config, workchain_id):
        path_to_md = 'sections/network.md'
        WorkchainDocSection.__init__(self, root_dir, path_to_md,
                                     config, workchain_id)

    def generate(self):
        d = {}
        return self.generate_content(d, append=False)
