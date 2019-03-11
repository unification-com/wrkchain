from string import Template

from workchain_sdk.utils import repo_root


class DocSection:
    def __init__(self, md_path):
        base_md_template_dir = 'templates/docs/md'
        self.root_dir = repo_root()

        self.template_path = self.root_dir / base_md_template_dir / md_path

        self.template = self.template_path.read_text()
        self.contents = ''

    def get_contents(self):
        return self.contents

    def add_content(self, d, append=True):
        t = Template(self.template)
        content = t.substitute(d)
        if append:
            self.contents += content
        else:
            self.contents = content
