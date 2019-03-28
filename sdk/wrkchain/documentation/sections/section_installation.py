from wrkchain.documentation.sections.doc_section import DocSection


class SectionInstallation(DocSection):
    def __init__(self, section_number, title, bootnode_config, base, nodes):
        path_to_md = 'installation.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__bootnode_config = bootnode_config
        self.__section_number = section_number
        self.__base = base
        self.__sub_section_number = 1
        self.__nodes = nodes

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
        md_file = 'sub/install/geth.md'
        t = self.load_sub_section_template(md_file)

        node_computers = ''
        for node in self.__nodes:
            node_computers += f'**{node["title"]}**: {node["ip"]}  \n'

        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number,
             '__NODE_COMPUTERS__': node_computers
             }
        )
        self.__sub_section_number += 1
        return contents

    def __install_geth_bootnode(self):
        contents = ''
        if self.__bootnode_config['type'] == 'dedicated':
            md_file = 'sub/install/geth_bootnode.md'
            t = self.load_sub_section_template(md_file)

            contents =  t.substitute(
                {'__SECTION_NUMBER__': self.__section_number,
                 '__SUB_SECTION_NUMBER__': self.__sub_section_number,
                 '__BOOTNODE_IP__': self.__bootnode_config['nodes']['ip']
                 }
            )
            self.__sub_section_number += 1

        return contents

    def __install_wrkchain_oracle(self):
        md_file = 'sub/install/wrkchain_oracle.md'
        t = self.load_sub_section_template(md_file)

        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents


class SectionInstallationBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, base, bootnode_config, nodes,
                 **_ignored):

        if not self.__instance:
            self.__instance = SectionInstallation(section_number,
                                                  title, bootnode_config,
                                                  base, nodes)

        return self.__instance
