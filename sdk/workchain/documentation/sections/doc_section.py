from string import Template

from workchain.utils import repo_root


class DocSection:
    def __init__(self, md_path, section_number, title):
        base_md_template_dir = 'templates/docs/md'
        self.root_dir = repo_root()

        self.template_path = self.root_dir / 'sdk' / base_md_template_dir \
                             / md_path

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
