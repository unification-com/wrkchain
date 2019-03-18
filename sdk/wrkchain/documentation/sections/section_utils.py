class SectionUtils:

    @staticmethod
    def set_geth_bootnode_flag(bootnode_address, bootnode_ip,
                               bootnode_port):
        bootnode_enode = f'enode://{bootnode_address}@' \
            f'{bootnode_ip}:' \
            f'{bootnode_port}'

        bootnode_flag = f'--bootnodes "' \
            f'{bootnode_enode}" '

        return bootnode_enode, bootnode_flag
