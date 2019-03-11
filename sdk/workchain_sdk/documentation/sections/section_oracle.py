from workchain_sdk.documentation.sections.doc_section import DocSection


class SectionOracle(DocSection):
    def __init__(self, oracle_addresses):
        path_to_md = 'sections/oracle.md'
        DocSection.__init__(self, path_to_md)

        self.__oracle_addresses = oracle_addresses

    def generate(self):
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses)
        }
        self.add_content(d, append=False)
        return self.get_contents()


class SectionOracleBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, oracle_addresses, **_ignored):

        if not self.__instance:
            self.__instance = SectionOracle(oracle_addresses)
        return self.__instance
