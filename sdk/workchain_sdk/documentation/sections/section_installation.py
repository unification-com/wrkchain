from workchain_sdk.documentation.sections.doc_section import DocSection


class SectionInstallationGeth(DocSection):
    def __init__(self):
        path_to_md = 'sections/install_geth.md'
        DocSection.__init__(self, path_to_md)

    def generate(self):
        d = {}
        self.add_content(d, append=False)
        return self.get_contents()


class SectionInstallationBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, base, **_ignored):

        if not self.__instance:
            if base == 'geth':
                self.__instance = SectionInstallationGeth()
            else:
                self.__instance = SectionInstallationGeth()

        return self.__instance
