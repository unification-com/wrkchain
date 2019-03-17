from wrkchain.documentation.sections.doc_section import DocSection


class SectionIntroduction(DocSection):
    def __init__(self, section_number, title, workchain_id):
        path_to_md = 'sections/introduction.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__workchain_id = workchain_id

    def generate(self):
        d = {
            '__WORKCHAIN_NETWORK_ID__': self.__workchain_id
        }
        self.add_content(d, append=False)
        return self.get_contents()


class SectionIntroductionBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, workchain_id, **_ignored):

        if not self.__instance:
            self.__instance = SectionIntroduction(section_number, title,
                                                  workchain_id)
        return self.__instance
