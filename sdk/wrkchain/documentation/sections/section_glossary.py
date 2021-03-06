from wrkchain.documentation.sections.doc_section import DocSection


class SectionGlossary(DocSection):
    def __init__(self, section_number, title):
        path_to_md = 'glossary.md'
        DocSection.__init__(self, path_to_md, section_number, title)

    def generate(self):
        d = {}
        self.add_content(d, append=False)
        return self.get_contents()


class SectionGlossaryBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, **_ignored):

        if not self.__instance:
            self.__instance = SectionGlossary(section_number, title)
        return self.__instance
