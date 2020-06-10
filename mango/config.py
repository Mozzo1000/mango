import os
import toml

FILE_PATH = 'mango.toml'


def generate_config(location=''):
    config_options = """
        [general]
        title = "Default site"
        base_url = "http://example.com"

        [build]
        content_folder = "content"
        template_folder = "templates"
        output_folder = "output"
        output_post_folder = "output/posts"
        static_folder = "static"
        ignore_files = ["layout.html", "post.html"]

        [sitemap]
        use_html_extension = "False"

        [server]
        host = "localhost"
        port = 8080
    """
    parsed_toml = toml.loads(config_options)
    with open(location + 'mango.toml', 'w') as config_file:
        config_file.write(toml.dumps(parsed_toml))


def get_config_file():
    return os.path.abspath(FILE_PATH)


def set_config_file(file='mango.toml'):
    global FILE_PATH
    FILE_PATH = file
    print(f'[CONFIG] Using config file: {file}')


def get_config():
    config = toml.load(FILE_PATH)
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
