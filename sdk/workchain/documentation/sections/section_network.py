from workchain.documentation.sections.doc_section import DocSection


class SectionNetwork(DocSection):
    def __init__(self, section_number, title, nodes):
        path_to_md = 'sections/network.md'
        DocSection.__init__(self, path_to_md, section_number, title)
        self.__nodes = nodes

    def generate(self):

        web3_urls = ''
        for node in self.__nodes:
            if node['rpc']:
                web3_urls += f'<http://{node["ip"]}:{node["rpc"]["port"]}>\n'

        d = {
            '__JSON_RPC_URLS__': web3_urls
        }

        self.add_content(d, append=False)
        return self.get_contents()


class SectionNetworkBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, nodes, **_ignored):

        if not self.__instance:
            self.__instance = SectionNetwork(section_number, title,
                                             nodes)

        return self.__instance
