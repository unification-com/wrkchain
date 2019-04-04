from wrkchain.documentation.sections.doc_section import DocSection
from wrkchain.utils import dir_tree


class SectionIntroduction(DocSection):
    def __init__(self, section_number, title, wrkchain_id, build_dir,
                 network, base, consensus, mainchain_rpc_uri):
        path_to_md = 'introduction.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__wrkchain_id = wrkchain_id
        self.__build_dir = build_dir
        self.__network = network
        self.__base = base
        self.__consensus = consensus
        self.__mainchain_rpc_uri = mainchain_rpc_uri

    def generate(self):

        testnet_warning = ''
        if self.__network == 'testnet':
            testnet_warning = self.__get_testnet_warning()

        mainchain_title = f'UND `{self.__network}`'
        und_json_rpc_note = self.__get_und_json_rpc_note()
        if self.__network == 'eth':
            mainchain_title = f'Ethereum `mainnet`'
            und_json_rpc_note = ''

        d = {
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__BUILD_DIR_STRUCTURE__': dir_tree(self.__build_dir),
            '__BASE_CHAIN__': self.__base,
            '__CONSENSUS__': self.__consensus,
            '__TESTNET_WARNING__': testnet_warning,
            '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
            '__MAINCHAIN_TITLE__': mainchain_title,
            '__UND_JSON_RPC_NOTE__': und_json_rpc_note
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __get_testnet_warning(self):
        testnet_md = f'{self.template_dir()}/sub/misc/intro_testnet_warning.md'
        testnet_md_path = self.root_dir / testnet_md
        return testnet_md_path.read_text()

    def __get_und_json_rpc_note(self):
        md_file = '/sub/introduction/und_json_rpc_note.md'
        t = self.load_sub_section_template(md_file)
        contents = t.substitute(
            {'__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
             '__MAINCHAIN_NETWORK__': self.__network})

        return contents


class SectionIntroductionBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, wrkchain_id, build_dir, network,
                 base, consensus, mainchain_rpc_uri, **_ignored):

        if not self.__instance:
            self.__instance = SectionIntroduction(section_number, title,
                                                  wrkchain_id, build_dir,
                                                  network, base, consensus,
                                                  mainchain_rpc_uri)
        return self.__instance
