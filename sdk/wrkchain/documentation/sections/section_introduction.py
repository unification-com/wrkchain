import os

from wrkchain.documentation.sections.doc_section import DocSection
from wrkchain.utils import dir_tree


class SectionIntroduction(DocSection):
    def __init__(self, section_number, title, wrkchain_id, build_dir,
                 network, base, consensus):
        path_to_md = 'introduction.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__wrkchain_id = wrkchain_id
        self.__build_dir = build_dir
        self.__network = network
        self.__base = base
        self.__consensus = consensus

    def generate(self):

        testnet_warning = ''
        if self.__network == 'testnet':
            testnet_warning = self.__get_testnet_warning()

        d = {
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__BUILD_DIR_STRUCTURE__': dir_tree(self.__build_dir),
            '__MAINCHAIN_NETWORK__': self.__network,
            '__BASE_CHAIN__': self.__base,
            '__CONSENSUS__': self.__consensus,
            '__TESTNET_WARNING__': testnet_warning
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __get_testnet_warning(self):
        testnet_md = f'{self.template_dir()}/sub/misc/intro_testnet_warning.md'
        testnet_md_path = self.root_dir / testnet_md
        return testnet_md_path.read_text()


class SectionIntroductionBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, wrkchain_id, build_dir, network,
                 base, consensus, **_ignored):

        if not self.__instance:
            self.__instance = SectionIntroduction(section_number, title,
                                                  wrkchain_id, build_dir,
                                                  network, base, consensus)
        return self.__instance
