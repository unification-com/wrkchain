from string import Template


class WorkchainDocSection:
    def __init__(self, root_dir, md_path, config, workchain_id):
        base_md_template_dir = 'templates/docs/md'

        self.root_dir = root_dir
        self.template_path = root_dir / base_md_template_dir / md_path
        self.config = config
        self.workchain_id = workchain_id

        self.template = None
        self.contents = ''
        self.data = None

        self.__load_template()

    def get_template(self):
        return self.template

    def get_contents(self):
        return self.contents

    def set_data(self, d):
        self.data = d

    def generate_content(self, d, append=True):
        self.set_data(d)
        t = Template(self.template)
        content = t.substitute(d)
        if append:
            self.contents += content
        else:
            self.contents = content
        return self.contents

    def __load_template(self):
        self.template = self.template_path.read_text()
