from workchain_sdk.documentation.sections.section import WorkchainDocSection


class WorkchainDocSectionInstallation(WorkchainDocSection):
    def __init__(self, root_dir, path_to_md, config, workchain_id):
        WorkchainDocSection.__init__(self, root_dir, path_to_md,
                                     config, workchain_id)
