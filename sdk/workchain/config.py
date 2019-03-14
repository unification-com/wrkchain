import json


class WorkchainConfig:
    def __init__(self, config_file):
        self.__overrides = {}
        self.__config = {}

        with open(config_file, 'r') as f:
            contents = f.read()
            self.__overrides = json.loads(contents)

        self.__load_overrides()

    def __load_overrides(self):
        self.__config = self.__overrides

    def get(self):
        return self.__config
