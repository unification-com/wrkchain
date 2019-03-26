from wrkchain.documentation.sections.doc_section import DocSection


class SectionOracle(DocSection):
    def __init__(self, section_number, title, oracle_addresses,
                 mainchain_rpc_uri, wrkchain_id, nodes,
                 oracle_write_frequency):

        path_to_md = 'oracle.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__oracle_addresses = oracle_addresses
        self.__mainchain_rpc_uri = mainchain_rpc_uri
        self.__wrkchain_id = wrkchain_id
        self.__nodes = nodes
        self.__oracle_write_frequency = oracle_write_frequency

    def generate(self):
        wrkchain_web3_provider = 'http://localhost:8545'
        web3_providers = []

        for node in self.__nodes:
            if node['rpc']:
                if isinstance(node['rpc'], bool):
                    rpc_port = '8545'
                else:
                    rpc_port = node["rpc"]["port"]
                web3_providers.append(f'http://{node["ip"]}:{rpc_port}')

        if web3_providers:
            wrkchain_web3_provider = ', '.join(web3_providers)
            if len(web3_providers) > 1:
                wrkchain_web3_provider = 'one of ' + wrkchain_web3_provider

        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses),
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
            '__ORACLE_WRITE_FREQUENCY__': self.__oracle_write_frequency,
            '__WRKCHAIN_WEB3_PROVIDER_URL__': wrkchain_web3_provider
        }
        self.add_content(d, append=False)
        return self.get_contents()


class SectionOracleBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, oracle_addresses,
                 mainchain_rpc_uri, wrkchain_id, nodes, oracle_write_frequency,
                 **_ignored):

        if not self.__instance:
            self.__instance = SectionOracle(section_number, title,
                                            oracle_addresses,
                                            mainchain_rpc_uri, wrkchain_id,
                                            nodes, oracle_write_frequency)
        return self.__instance
