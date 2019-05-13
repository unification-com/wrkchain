from wrkchain.documentation.sections.doc_section import DocSection


class SectionOracle(DocSection):
    def __init__(self, section_number, title, oracle_addresses,
                 mainchain_rpc_uri, wrkchain_id, nodes,
                 oracle_write_frequency, network, build_dir, oracle_hashes):

        path_to_md = 'oracle.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__oracle_addresses = oracle_addresses
        self.__mainchain_rpc_uri = mainchain_rpc_uri
        self.__wrkchain_id = wrkchain_id
        self.__nodes = nodes
        self.__oracle_write_frequency = oracle_write_frequency
        self.__network = network
        self.__build_dir = build_dir
        self.__oracle_hashes = oracle_hashes

    def generate(self):
        default_wrkchain_web3_provider = '[YOUR_WRKCHAIN_JSON_RPC_URL]'
        web3_providers = []

        for node in self.__nodes:
            if node['rpc']:
                if isinstance(node['rpc'], bool):
                    rpc_port = '8545'
                else:
                    rpc_port = node["rpc"]["port"]
                web3_providers.append(f'http://{node["ip"]}:{rpc_port}')

        if web3_providers:
            default_wrkchain_web3_provider = web3_providers[0]

        if self.__network == 'eth':
            network_title = 'Ethereum mainnet'
        else:
            network_title = f'UND {self.__network}'

        oracle_hashes_list = self.__oracle_hashes.split(",")
        oracle_hashes = ''
        for oh in oracle_hashes_list:
            oracle_hashes = f'{oracle_hashes}  --hash.{oh} \\ \n'

        d = {
            '__ORACLE_ADDRESSES__': '\n'.join(self.__oracle_addresses),
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
            '__ORACLE_WRITE_FREQUENCY__': self.__oracle_write_frequency,
            '__WRKCHAIN_WEB3_PROVIDER_URL__': default_wrkchain_web3_provider,
            '__MAINCHAIN_NETWORK_TITLE__': network_title,
            '__BUILD_DIR__': self.__build_dir,
            '__ORACLE_DATA_DIR__': '.wrkchain_oracle',
            '__MAIN_ORACLE_ADDRESS__': self.__oracle_addresses[0],
            '__ORACLE_ADDRESSES_CMD__': ','.join(self.__oracle_addresses),
            '__ORACLE_HASHES__': oracle_hashes.rstrip('\n')

        }
        self.add_content(d, append=False)
        return self.get_contents()


class SectionOracleBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, oracle_addresses,
                 mainchain_rpc_uri, wrkchain_id, nodes, oracle_write_frequency,
                 network, build_dir, oracle_hashes, **_ignored):

        if not self.__instance:
            self.__instance = SectionOracle(section_number, title,
                                            oracle_addresses,
                                            mainchain_rpc_uri, wrkchain_id,
                                            nodes, oracle_write_frequency,
                                            network, build_dir, oracle_hashes)
        return self.__instance
