from wrkchain.documentation.sections.doc_section import DocSection


class SectionBootNodes(DocSection):
    def __init__(self, section_number, title, bootnode_config, build_dir):
        path_to_md = 'bootnode.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__bootnode_config = bootnode_config
        self.__build_dir = build_dir

    def generate(self):
        if self.__bootnode_config['type'] == 'dedicated':
            bootnode = self.__bootnode_config['nodes']

            d = {'__BOOTNODE_ENODE': bootnode['enode'],
                 '__BOOTNODE_PORT': bootnode['port'],
                 '__BUILD_DIR__': self.__build_dir.replace('../', '')
                 }

            self.add_content(d, append=False)
            return self.get_contents()
        else:
            return ''


class SectionBootNodesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, bootnode_config, build_dir,
                 **_ignored):

        if not self.__instance:
            self.__instance = SectionBootNodes(section_number, title,
                                               bootnode_config, build_dir)
        return self.__instance
