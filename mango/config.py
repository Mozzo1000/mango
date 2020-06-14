import os
import toml
from mango.defaults import default_config_options

FILE_PATH = 'mango.toml'


def generate_config(location=''):
    config_options = default_config_options
    parsed_toml = toml.loads(config_options)
    with open(location + 'mango.toml', 'w') as config_file:
        config_file.write(toml.dumps(parsed_toml))


def get_config_file():
    return os.path.abspath(FILE_PATH)


def set_config_file(file='mango.toml', use_default=False):
    global FILE_PATH
    FILE_PATH = file
    if use_default:
        print('[CONFIG] No config file found, using default config')
    else:
        print(f'[CONFIG] Using config file: {file}')


def get_config():
    if os.path.isfile(FILE_PATH):
        config = toml.load(FILE_PATH)
    else:
        config = toml.loads(FILE_PATH)
    return config


def get_config_setting(section, setting):
    config = get_config()
    return config[section][setting]


def check_config_exists(location=''):
    if os.path.isfile(location + 'mango.toml'):
        return "OTHER_DIR"
    elif os.path.isfile('mango.toml'):
        return True
    else:
        return False
