import configparser
import os

FILE_PATH = 'mango.ini'


def generate_config(title, location=''):
    config = configparser.ConfigParser()
    config.add_section('general')
    config.set('general', 'title', title)
    config.set('general', 'content_folder', 'content')
    config.set('general', 'template_folder', 'templates')
    config.set('general', 'output_folder', 'output')
    config.set('general', 'output_post_folder', 'output/posts')
    config.set('general', 'static_folder', 'static')

    config.add_section('server')
    config.set('server', 'host', 'localhost')
    config.set('server', 'port', '8080')

    with open(location + 'mango.ini', 'w') as config_file:
        config.write(config_file)


def get_config_file():
    return os.path.abspath(FILE_PATH)


def set_config_file(file='mango.ini'):
    global FILE_PATH
    FILE_PATH = file


def get_config():
    config = configparser.ConfigParser()
    config.read(FILE_PATH)
    return config


def get_config_setting(section, setting, fallback=None):
    config = get_config()
    return config.get(section, setting, fallback=fallback)


def check_config_exists(location=''):
    if os.path.isfile(location + 'mango.ini'):
        return "OTHER_DIR"
    elif os.path.isfile('mango.ini'):
        return True
    else:
        return False
