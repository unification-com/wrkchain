GETH_PATH = '$GOPATH/bin/geth'


def generate_geth_cmd(
        node, bootnode_config, wrkchain_id, listen_port, linebreak=False):

    flags = []

    if bootnode_config['type'] == 'dedicated':
        flags.append(f'--bootnodes {bootnode_config["nodes"]["enode"]}"')
    else:
        flags.append(f'--nodekey="/root/node_keys/{node["address"]}.key"')

    flags = flags + [
        f'--port {listen_port}',
        f'--networkid {wrkchain_id}',
        f'--syncmode=full',
        f'--verbosity=4'
    ]

    if node['is_validator']:
        flags = flags + [
            f'--gasprice "0"',
            f'--etherbase {node["address"]}',
            f'--password /root/.walletpassword',
            f'--mine',
            f'--unlock {node["address"]}',
        ]

    if node['rpc']:
        apis = []
        for api, use_api in node['rpc']['apis'].items():
            if use_api:
                apis.append(api)
        rpc_port = node["rpc"]["port"]
        rpcaddr = node["rpc"]["rpcaddr"]
        rpccorsdomain = node["rpc"]["rpccorsdomain"]
        rpcvhosts = node["rpc"]["rpcvhosts"]
        flags = flags + [
            f'--rpc',
            f'--rpcaddr "{rpcaddr}"',
            f'--rpcport "{rpc_port}"',
            f'--rpcapi "{",".join(apis)}"',
            f'--rpccorsdomain "{rpccorsdomain}"',
            f'--rpcvhosts "{rpcvhosts}"']

    flags = sorted(flags)
    if linebreak:
        options = ' \\\n\t'.join(flags)
    else:
        options = ' '.join(flags)

    return f"{GETH_PATH} {options}"
