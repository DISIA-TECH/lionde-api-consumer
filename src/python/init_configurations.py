import configparser

class ConfigLoader:
    def __init__(self, config_file: str = "src/resources/config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def getattr(self, key, section: str = "my_section"):
        return self.config.get(section, key)
