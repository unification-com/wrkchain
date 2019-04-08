from wrkchain.constants import DEFAULT_WRKCHAIN_DATA_DIR
from wrkchain.documentation.sections.doc_section import DocSection


class SectionNetwork(DocSection):
    def __init__(self, section_number, title, nodes, build_dir,
                 bootnode_config, wrkchain_id):
        path_to_md = 'network.md'
        DocSection.__init__(self, path_to_md, section_number, title)
        self.__nodes = nodes
        self.__build_dir = build_dir
        self.__bootnode_config = bootnode_config
        self.__wrkchain_id = wrkchain_id
        self.__section_number = section_number
        self.__sub_section_number = 1

    def generate(self):

        web3_providers = []
        for node in self.__nodes:
            if node['rpc']:
                rpc = {
                    'ip': node["ip"],
                    'port': node["rpc"]["port"],
                    'title': node['title']
                }
                web3_providers.append(rpc)

        configured_rpc_nodes = self.__configured_json_rpc_nodes(web3_providers)

        d = {
            '__CONFIGURED_JSON_RPC_NODES__': configured_rpc_nodes,
            '__RUNNING_LOCAL_JSON_RPC_NODE__':
                self.__running_local_json_rpc_node()
        }

        self.add_content(d, append=False)
        return self.get_contents()

    def __configured_json_rpc_nodes(self, web3_providers):
        contents = ''
        if len(web3_providers) > 0:
            md_file = 'sub/network/configured_json_rpc_nodes.md'
            t = self.load_sub_section_template(md_file)
            web3_provider_output = ''
            for web3 in web3_providers:
                web3_provider_output += f'**{web3["title"]}**  \n' \
                    f'**Web3 Provider URL:**<http://{web3["ip"]}:' \
                    f'{web3["port"]}>  \n' \
                    f'**Web3 Provider Host:** {web3["ip"]}  \n' \
                    f'**Web3 Provider Port:** {web3["port"]}  \n' \
                    f'**Network ID:** {self.__wrkchain_id}\n\n'

            d = {
                '__SECTION_NUMBER__': self.__section_number,
                '__SUB_SECTION_NUMBER__': self.__sub_section_number,
                '__WEB3_PROVIDERS__': web3_provider_output
            }
            contents = t.substitute(d)
            self.__sub_section_number += 1

        return contents

    def __running_local_json_rpc_node(self):
        doc_build_dir = self.__build_dir.replace('../', '')
        md_file = 'sub/network/local_json_rpc_node.md'
        t = self.load_sub_section_template(md_file)

        copy_static_files = ''

        if self.__bootnode_config['type'] == 'static':
            copy_static_files = f'2. `{doc_build_dir}/static-nodes.json` to ' \
                f'`$HOME/{DEFAULT_WRKCHAIN_DATA_DIR}/static-nodes.json`  \n'

        geth_cmd = f'$GOPATH/bin/geth --networkid {self.__wrkchain_id} \\\n' \
            f'--rpc \\\n' \
            f'--rpcapi "eth,personal,web3" \\\n' \
            f'--rpcport "8550" \\\n' \
            f'--syncmode=light \\\n' \
            f'--verbosity=4'

        d = {
            '__SECTION_NUMBER__': self.__section_number,
            '__SUB_SECTION_NUMBER__': self.__sub_section_number,
            '__BUILD_DIR__': doc_build_dir,
            '__COPY_STATIC_FILES__': copy_static_files,
            '__GETH_COMMAND__': geth_cmd,
            '__WRKCHAIN_NETWORK_ID__': self.__wrkchain_id,
            '__WRKCHAIN_DATA_DIR__': DEFAULT_WRKCHAIN_DATA_DIR
        }

        contents = t.substitute(d)
        self.__sub_section_number += 1
        return contents


class SectionNetworkBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, nodes, build_dir,
                 bootnode_config, wrkchain_id, **_ignored):

        if not self.__instance:
            self.__instance = SectionNetwork(section_number, title,
                                             nodes, build_dir, bootnode_config,
                                             wrkchain_id)

        return self.__instance
