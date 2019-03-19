from string import Template

from wrkchain.documentation.sections.doc_section import DocSection


class SectionInstallationGeth(DocSection):
    def __init__(self, section_number, title, bootnode_config):
        path_to_md = 'sections/install_geth.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__bootnode_config = bootnode_config
        self.__section_number = section_number

    def generate(self):
        install_bootnode_content = ""
        if self.__bootnode_config['type'] == 'dedicated':
            install_bootnode_md = f'templates/docs/md/sections/' \
                f'install_geth_bootnode.md'
            install_bootnode_md_path = self.root_dir / install_bootnode_md
            install_bootnode = install_bootnode_md_path.read_text()
            t = Template(install_bootnode)
            install_bootnode_content = \
                t.substitute({'__SECTION_NUMBER__': self.__section_number})

        d = {
            '__INSTALL_GETH_BOOTNODE__': install_bootnode_content
        }
        self.add_content(d, append=False)
        return self.get_contents()


class SectionInstallationBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, base, bootnode_config,
                 **_ignored):

        if not self.__instance:
            if base == 'geth':
                self.__instance = SectionInstallationGeth(section_number,
                                                          title,
                                                          bootnode_config)
            else:
                self.__instance = SectionInstallationGeth(section_number,
                                                          title,
                                                          bootnode_config)

        return self.__instance
