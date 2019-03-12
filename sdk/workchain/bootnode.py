import os
import shutil
import subprocess

BIN_BOOTNODE = shutil.which("bootnode")


class BootnodeKey:
    def __init__(self, build_dir, ip, port, key_prefix=''):
        # Todo - throw exception if BIN_BOOTNODE not found/empty
        self.__bootnode_key_path = build_dir + f'/{key_prefix}bootnode.key'
        self.__ip = ip
        self.__port = port

    def generate_bootnode_key(self):
        if not self.have_key():

            cmd = [BIN_BOOTNODE, "-genkey", self.__bootnode_key_path]
            result = self.__run(cmd)
            if result.returncode == 0:
                os.chmod(self.__bootnode_key_path, 0o666)
            else:
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
