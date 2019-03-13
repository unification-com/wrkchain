from workchain.documentation.sections.doc_section import DocSection


class SectionInstallationGeth(DocSection):
    def __init__(self, section_number, title):
        path_to_md = 'sections/install_geth.md'
        DocSection.__init__(self, path_to_md, section_number, title)

    def generate(self):
        d = {}
        self.add_content(d, append=False)
        return self.get_contents()


class SectionInstallationBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, base, **_ignored):

        if not self.__instance:
            if base == 'geth':
                self.__instance = SectionInstallationGeth(section_number,
                                                          title)
            else:
                self.__instance = SectionInstallationGeth(section_number,
                                                          title)

        return self.__instance
