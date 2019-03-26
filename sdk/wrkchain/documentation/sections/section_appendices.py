from string import Template

from wrkchain.documentation.sections.doc_section import DocSection


class SectionAppendices(DocSection):
    def __init__(self, section_number, title):
        path_to_md = 'appendices.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__section_number = section_number
        self.__sub_section_number = 1

    def generate(self):

        appendix_1 = self.__appendix_1()
        appendix_2 = self.__appendix_2()

        d = {
            '__APPENDIX_1__': appendix_1,
            '__APPENDIX_2__': appendix_2,
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __appendix_1(self):
        appendix_md = f'{self.template_dir()}/sub/appendices/appendix1.md'
        appendix_md_path = self.root_dir / appendix_md
        appendix = appendix_md_path.read_text()
        t = Template(appendix)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents

    def __appendix_2(self):
        appendix_md = f'{self.template_dir()}/sub/appendices/appendix2.md'
        appendix_md_path = self.root_dir / appendix_md
        appendix = appendix_md_path.read_text()
        t = Template(appendix)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents


class SectionAppendicesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, **_ignored):
        if not self.__instance:
            self.__instance = SectionAppendices(section_number, title)

        return self.__instance
