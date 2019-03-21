from wrkchain.documentation.sections.doc_section import DocSection


class SectionOracle(DocSection):
    def __init__(self, section_number, title, oracle_addresses,
                 mainchain_rpc_uri, wrkchain_id, nodes):
        path_to_md = 'sections/oracle.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__oracle_addresses = oracle_addresses
        self.__mainchain_rpc_uri = mainchain_rpc_uri
        self.__wrkchain_id = wrkchain_id
        self.__nodes = nodes

    def generate(self):
        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses),
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri
        }
        self.add_content(d, append=False)
        return self.get_contents()


class SectionOracleBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, oracle_addresses,
                 mainchain_rpc_uri, wrkchain_id, nodes, **_ignored):

        if not self.__instance:
            self.__instance = SectionOracle(section_number, title,
                                            oracle_addresses,
                                            mainchain_rpc_uri, wrkchain_id,
                                            nodes)
        return self.__instance
