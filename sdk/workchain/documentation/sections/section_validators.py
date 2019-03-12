from workchain.documentation.sections.doc_section import DocSection


class SectionValidators(DocSection):
    def __init__(self, section_number, title, validators, workchain_id,
                 bootnode_config):
        path_to_md = 'sections/validators.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__validators = validators
        self.__workchain_id = workchain_id
        self.__bootnode_config = bootnode_config

    def generate(self):
        if self.__bootnode_config['type'] == 'dedicated':
            bootnode_flag = f'--bootnodes "' \
                f'{self.__bootnode_config["nodes"]["enode"]}" '
        else:
            bootnode_flag = ''

        for i in range(len(self.__validators)):
            d = {'__VALIDATOR_NUM__': str(i + 1),
                 '__WORKCHAIN_NETWORK_ID__': str(self.__workchain_id),
                 '__BOOTNODE__': bootnode_flag,
                 '__EV_PUBLIC_ADDRESS__': self.__validators[i]['address']
                 }
            self.add_content(d, append=True)

        return self.get_contents()


class SectionValidatorsBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, validators, workchain_id,
                 bootnode_config, **_ignored):
        if not self.__instance:
            self.__instance = SectionValidators(section_number, title,
                                                validators, workchain_id,
                                                bootnode_config)
        return self.__instance
