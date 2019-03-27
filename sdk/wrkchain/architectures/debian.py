GETH_PATH = '/bin/geth'


def generate_geth_cmd(
        node, bootnode_config, wrkchain_id, listen_port, linebreak=False,
        gopath='/root/.go', docker=True, path_to='/root'):

    key_prefix = ''
    if docker:
        key_prefix = 'docker_'

    flags = []

    if bootnode_config['type'] == 'dedicated':
        flags.append(f'--bootnodes '
                     f'"{bootnode_config["nodes"][key_prefix + "enode"]}"')
    else:
        flags.append(f'--nodekey="{path_to}/node_keys/{node["address"]}.key"')

    flags = flags + [
        f'--port {listen_port}',
        f'--networkid {wrkchain_id}',
        f'--syncmode=full',
        f'--verbosity=4'
    ]

    if docker:
        wallet_password = f'{path_to}/.walletpassword'
    else:
        wallet_password = 'YOUR_WALLET_PASSWORD'

    if node['is_validator']:
        flags = flags + [
            f'--gasprice "0"',
            f'--etherbase {node["address"]}',
            f'--password {wallet_password}',
            f'--mine',
            f'--unlock {node["address"]}',
        ]

    if node['rpc']:
        apis = []
        for api, use_api in node['rpc']['apis'].items():
            if use_api:
                apis.append(api)
        rpc_port = node["rpc"][key_prefix + "port"]
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

    return f"{gopath}{GETH_PATH} {options}"
