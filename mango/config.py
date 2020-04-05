import configparser
import os


def generate_config(head_partial, layout_file, foot_partial, location=''):
    config = configparser.ConfigParser()
    config.add_section('partials')
    config.set('partials', 'header', head_partial)
    config.set('partials', 'footer', foot_partial)

    config.add_section('layout')
    config.set('layout', 'default', layout_file)

    with open(location + 'mango.ini', 'w') as config_file:
        config.write(config_file)


def get_config(file='mango.ini'):
    config = configparser.ConfigParser()
    config.read(file)
    return config


def get_config_setting(section, setting, file_override=None):
    if file_override:
        config = get_config(file=file_override)
    else:
        config = get_config()
    return config.get(section, setting)


def check_config_exists():
    return os.path.isfile('mango.ini')