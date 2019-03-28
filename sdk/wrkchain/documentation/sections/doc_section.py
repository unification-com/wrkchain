from string import Template

from wrkchain.utils import repo_root


class DocSection:
    def __init__(self, md_path, section_number, title):
        self.__template_dir = 'templates/docs/md/sections/'
        self.root_dir = repo_root()

        self.template_path = self.root_dir / \
            self.__template_dir / md_path

        self.template = self.template_path.read_text()
        self.contents = ''
        self.title = ''
        self.section_number = section_number
        self.set_title(section_number, title)

    def generate(self): pass
    
    def get_title(self):
        return self.title

    def get_contents(self):
        return f'{self.title}\n\n{self.contents}'

    def template_dir(self):
        return self.__template_dir

    def set_title(self, section_number, title):
        self.title = f'## {section_number}. {title}'

    def add_content(self, d, append=True):
        # inject section number
        d['__SECTION_NUMBER__'] = self.section_number
        t = Template(self.template)
        content = t.substitute(d)
        if append:
            self.contents += content
        else:
            self.contents = content

    def load_sub_section_template(self, md_file):
        md = f'{self.template_dir()}/{md_file}'
        md_path = self.root_dir / md
        md_content = md_path.read_text()
        return Template(md_content)
