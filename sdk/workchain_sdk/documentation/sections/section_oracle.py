from workchain_sdk.documentation.sections.section import WorkchainDocSection


class WorkchainDocSectionOracle(WorkchainDocSection):
    def __init__(self, root_dir, config, workchain_id):
        path_to_md = 'sections/oracle.md'
        WorkchainDocSection.__init__(self, root_dir, path_to_md,
                                     config, workchain_id)

    def generate(self, oracle_addresses):
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(oracle_addresses)
        }
        return self.generate_content(d, append=False)
