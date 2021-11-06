import configparser


class Config:

    def __init__(self, read_file, setting=None):
        self.read_file = read_file
        self.setting = setting
        self.config = self.get_config_file(setting)

    def get_config_file(self, setting):
        self.config = configparser.ConfigParser()
        self.config.read(self.read_file)
        self.config = {section: dict(self.config[section]) for section in self.config.sections()}
        self.config = self.config[setting]
        return self.config
