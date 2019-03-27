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
        d = {
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__BUILD_DIR_STRUCTURE__': dir_tree(self.__build_dir),
            '__MAINCHAIN_NETWORK__': self.__network,
            '__BASE_CHAIN__': self.__base,
            '__CONSENSUS__': self.__consensus
        }
        self.add_content(d, append=False)
        return self.get_contents()


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
