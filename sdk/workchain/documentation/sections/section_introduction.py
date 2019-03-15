from workchain.documentation.sections.doc_section import DocSection


class SectionIntroduction(DocSection):
    def __init__(self, section_number, title):
        path_to_md = 'sections/introduction.md'
        DocSection.__init__(self, path_to_md, section_number, title)

    def generate(self):
        d = {}
        self.add_content(d, append=False)
        return self.get_contents()


class SectionIntroductionBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, oracle_addresses, **_ignored):

        if not self.__instance:
            self.__instance = SectionIntroduction(section_number, title)
        return self.__instance
