import ConfigParser
import os

config = None
config_path = '/etc/amie-processing'
config_file = 'amie-processing.cfg'

def get_config():
    global config
    if config is None:
        config = ConfigParser.ConfigParser()
        with open(os.path.join(config_path, config_file)) as source:
            config.readfp(source)
    return config

        
        