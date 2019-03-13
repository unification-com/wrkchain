from workchain.documentation.sections.doc_section import DocSection


class SectionNodes(DocSection):
    def __init__(self, section_number, title, nodes, workchain_id,
                 bootnode_config):
        path_to_md = 'sections/nodes.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__nodes = nodes
        self.__workchain_id = workchain_id
        self.__bootnode_config = bootnode_config

    def generate(self):
        for i in range(len(self.__nodes)):
            node_types = []
            node = self.__nodes[i]

            public_address = node['address']
            listen_port = node['listen_port']
            copy_static_nodes_json = ''

            # common flags
            listen_port_flag = f' --port {listen_port}'
            network_id_flag = f' --networkid "{str(self.__workchain_id)}"'
            verbosity_flag = ' --verbosity=4'
            syncmode_flag = ' --syncmode=full'

            if self.__bootnode_config['type'] == 'dedicated':
                bootnode_flag = f' --bootnodes "' \
                    f'{self.__bootnode_config["nodes"]["enode"]}" '
            else:
                bootnode_flag = f' --nodekey="path/to/{public_address}.key"'
                copy_static_nodes_json = 'Copy `build/static-nodes.json` to' \
                                         '`~/.ethereum`'

            # Validator only
            if node['is_validator']:
                validator_flags = f' --mine' \
                    f' --gasprice "0"' \
                    f' --etherbase {public_address}' \
                    f' --unlock {public_address}' \
                    f' --password WALLET_PASSWORD'
                node_types.append('Validator')
            else:
                validator_flags = ''

            # RPC only
            if node['rpc']:
                apis = []
                for api, use_api in node['rpc']['apis'].items():
                    if use_api:
                        apis.append(api)

                rpc_flags = f' --rpc' \
                    f' --rpcaddr "0.0.0.0"' \
                    f' --rpcport "{node["rpc"]["port"]}"' \
                    f' --rpcapi "{",".join(apis)}"' \
                    f' --rpccorsdomain "*"'

                node_types.append('JSON RPC')
            else:
                rpc_flags = ''

            geth_cmd = f'geth {bootnode_flag}{network_id_flag}' \
                f'{verbosity_flag}{syncmode_flag}{validator_flags}' \
                f'{rpc_flags}{listen_port_flag}'

            d = {'__NODE_NUM__': str(i + 1),
                 '__EV_PUBLIC_ADDRESS__': public_address,
                 '__GETH_COMMAND__': geth_cmd,
                 '__NODE_TYPE__': ' & '.join(node_types),
                 '__NODE_NAME__': node['id'],
                 '__COPY_STATIC_NODES_JSON__': copy_static_nodes_json
                 }
            self.add_content(d, append=True)

        return self.get_contents()


class SectionNodesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, nodes, workchain_id,
                 bootnode_config, **_ignored):
        if not self.__instance:
            self.__instance = SectionNodes(section_number, title,
                                           nodes, workchain_id,
                                           bootnode_config)
        return self.__instance
