from workchain_sdk.documentation.sections.section_installation \
    import WorkchainDocSectionInstallation


class WorkchainDocSectionInstallationGeth(WorkchainDocSectionInstallation):
    def __init__(self, root_dir, config, workchain_id):
        path_to_md = 'sections/install_geth.md'

        WorkchainDocSectionInstallation.__init__(self, root_dir,
                                                 path_to_md, config,
                                                 workchain_id)

    def generate(self):
        return self.generate_content({}, append=False)
