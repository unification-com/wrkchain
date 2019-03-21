import os
import shutil
import subprocess

BIN_BOOTNODE = shutil.which("bootnode")


class BootnodeKey:
    def __init__(self, build_dir, ip, port, key_prefix=''):
        # Todo - throw exception if BIN_BOOTNODE not found/empty
        if len(key_prefix) > 0:
            key_prefix = f'{key_prefix}'
        else:
            key_prefix = 'bootnode'

        node_dir = build_dir + '/node_keys'
        if not os.path.exists(node_dir):
            os.makedirs(node_dir)

        self.__bootnode_key_path = node_dir + f'/{key_prefix}.key'
        self.__ip = ip
        self.__port = port

    def generate_bootnode_key(self):
        if not self.have_key():

            cmd = [BIN_BOOTNODE, "-genkey", self.__bootnode_key_path]
            result = self.__run(cmd)
            print(result)

    def get_bootnode_address(self):
        if not self.have_key():
            self.generate_bootnode_key()

        cmd = [BIN_BOOTNODE, "-nodekey",
               self.__bootnode_key_path, "-writeaddress"]

        result = self.__run(cmd)

        if result.returncode == 0:
            bootnode_address = result.stdout.rstrip("\n\r")
        else:
            print(result)
            bootnode_address = None

        return bootnode_address

    def get_enode(self):
        if not self.have_key():
            self.generate_bootnode_key()

        return f'enode://{self.get_bootnode_address()}@{self.__ip}' \
            f':{self.__port}'

    def have_key(self):
        return os.path.exists(self.__bootnode_key_path)

    def __run(self, cmd):
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        return result
