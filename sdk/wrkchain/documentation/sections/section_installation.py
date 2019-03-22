from string import Template

from wrkchain.documentation.sections.doc_section import DocSection


class SectionInstallation(DocSection):
    def __init__(self, section_number, title, bootnode_config, base):
        path_to_md = 'installation.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__bootnode_config = bootnode_config
        self.__section_number = section_number
        self.__base = base
        self.__sub_section_number = 1

    def generate(self):

        install_node = ''
        install_bootnode = ''

        if self.__base == 'geth':
            install_node = self.__install_geth()
            install_bootnode = self.__install_geth_bootnode()
        
        d = {
            '__INSTALL_NODES__': install_node,
            '__INSTALL_BOOTNODE__': install_bootnode,
            '__INSTALL_WRKCHAIN_ORACLE__': self.__install_wrkchain_oracle()
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __install_geth(self):
        install_md = f'{self.template_dir()}/sub/install/geth.md'
        install_md_path = self.root_dir / install_md
        install_geth = install_md_path.read_text()
        t = Template(install_geth)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents

    def __install_geth_bootnode(self):
        contents = ''
        if self.__bootnode_config['type'] == 'dedicated':
            install_md = f'{self.template_dir()}/sub/install/' \
                f'geth_bootnode.md'
            install_md_path = self.root_dir / install_md
            install_bootnode = install_md_path.read_text()
            t = Template(install_bootnode)
            contents =  t.substitute(
                {'__SECTION_NUMBER__': self.__section_number,
                 '__SUB_SECTION_NUMBER__': self.__sub_section_number})
            self.__sub_section_number += 1

        return contents

    def __install_wrkchain_oracle(self):
        install_md = f'{self.template_dir()}/sub/install/' \
            f'wrkchain_oracle.md'
        install_md_path = self.root_dir / install_md
        install_oracle = install_md_path.read_text()
        t = Template(install_oracle)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents


class SectionInstallationBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, base, bootnode_config,
                 **_ignored):

        if not self.__instance:
            self.__instance = SectionInstallation(section_number,
                                                  title, bootnode_config, base)

        return self.__instance
