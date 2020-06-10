from argparse import ArgumentParser
import markdown2
import os
import shutil
import sys
import time
import htmlmin
import rjsmin
from csscompressor import compress
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from distutils.dir_util import copy_tree
from mango.defaults import create_default_files
from mango.config import get_config_setting, generate_config, check_config_exists, set_config_file, get_config_file
from http.server import HTTPServer
from mango.httpserver import SimpleServer, WebServer
from mango.sitemap import Sitemap
from mango.generator import Generator

SITE_TITLE = ''
CONTENT_FOLDER = ''
TEMPLATE_FOLDER = ''
OUTPUT_FOLDER = ''
OUTPUT_POST_FOLDER = ''
STATIC_FOLDER = ''
BASE_URL = ''

WORKING_PATH = ''


def main():
    parser = ArgumentParser(description='')
    parser.add_argument('path', default='')
    parser.add_argument('--config', help='Config file')
    parser.add_argument('--generate-config', help='Generate config file', action='store_true')
    parser.add_argument('--create-project', help='Create a default project folder structure')
    parser.add_argument('--server', help='Run a development server', action='store_true')
    parser.add_argument('--rebuild', help='Rebuilds all files', action='store_true')
    parser.add_argument('--minify', help='Minifies HTML, CSS and JS files', action='store_true')
    parser.add_argument('--watch', help='Watch directory and automatically rebuild', action='store_true')

    global WORKING_PATH

    if parser.parse_args().path:
        working_path = parser.parse_args().path
        WORKING_PATH = working_path
        if parser.parse_args().path is '.':
            working_path = os.getcwd() + '/'
        print('PATH SUPPLIED: ' + working_path)

    global SITE_TITLE
    global CONTENT_FOLDER
    global TEMPLATE_FOLDER
    global OUTPUT_FOLDER
    global OUTPUT_POST_FOLDER
    global STATIC_FOLDER
    global BASE_URL

    if parser.parse_args().config:
        set_config_file(parser.parse_args().config)
    if check_config_exists(location=working_path):
        if check_config_exists(location=working_path) == 'OTHER_DIR':
            set_config_file(working_path + 'mango.ini')
        print('Using config file: ' + get_config_file())
    else:
        print('No config file found, falling back to defaults.')

    SITE_TITLE = get_config_setting('general', 'title', fallback='Default site')
    CONTENT_FOLDER = get_config_setting('build', 'content_folder', fallback='content')
    TEMPLATE_FOLDER = get_config_setting('build', 'template_folder', fallback='templates')
    OUTPUT_FOLDER = get_config_setting('build', 'output_folder', fallback='output')
    OUTPUT_POST_FOLDER = get_config_setting('build', 'output_post_folder', fallback='output/posts')
    STATIC_FOLDER = get_config_setting('build', 'static_folder', fallback='static')
    BASE_URL = get_config_setting('general', 'base_url', fallback='http://example.com')

    SERVER_HOST = get_config_setting('server', 'host', fallback='localhost')
    SERVER_PORT = get_config_setting('server', 'port', fallback='8080')

    if parser.parse_args().rebuild:
        rebuild(True if parser.parse_args().minify is True else False, folder=working_path)
    elif parser.parse_args().create_project:
        project_name = parser.parse_args().create_project
        if os.path.exists(project_name):
            print('Folder already exists, please use a non existing folder.')
        else:
            os.makedirs(project_name)
            os.makedirs(project_name + '/content')
            os.makedirs(project_name + '/static')
            os.makedirs(project_name + '/templates')
            generate_config(title='Default site', location=project_name + '/')
            create_default_files(project_name)
    elif parser.parse_args().generate_config:
        generate_config('Default site', '')

    if parser.parse_args().server and parser.parse_args().watch:
        try:
            server = WebServer(SERVER_HOST, SERVER_PORT)
            event_handler = PatternMatchingEventHandler(patterns='*', ignore_patterns=['output/*'],
                                                        ignore_directories=True)
            event_handler.on_modified = watch_on_modified
            observer = Observer()
            observer.schedule(event_handler, working_path, recursive=True)
            observer.start()
            print('[WATCHER] Started watcher')
            server.start_server()
        except KeyboardInterrupt:
            server.stop_server()
            observer.stop()
        observer.join()

    if parser.parse_args().server:
        try:
            server = WebServer(SERVER_HOST, SERVER_PORT, working_path)
            server.start_server()
        except KeyboardInterrupt:
            server.stop_server()
    if parser.parse_args().watch:
        try:
            event_handler = PatternMatchingEventHandler(patterns='*', ignore_patterns=['output/*'], ignore_directories=True)
            event_handler.on_modified = watch_on_modified
            observer = Observer()
            observer.schedule(event_handler, working_path, recursive=True)
            observer.start()
            print('[WATCHER] Started watcher')
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


def rebuild(minify, folder=''):
    start_time = time.perf_counter()
    POSTS = {}

    current_date = str(datetime.date(datetime.now()))
    sitemap = Sitemap(folder + OUTPUT_FOLDER)

    for markdown_post in os.listdir(folder + CONTENT_FOLDER):
        if markdown_post.endswith('.md'):
            file_path = os.path.join(folder + CONTENT_FOLDER, markdown_post)
            with open(file_path, 'r') as file:
                POSTS[markdown_post] = markdown2.markdown(file.read(), extras=['metadata', 'cuddled-lists'])

    POSTS = {
        post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
    }
    create_output_folder(dir=folder + OUTPUT_FOLDER, overwrite=True)

    posts_metadata = [POSTS[post].metadata for post in POSTS]

    page = Generator(folder + OUTPUT_FOLDER, folder + 'templates', BASE_URL,
                     posts_metadata, sitemap, site_title=SITE_TITLE,
                     minify_code=minify)

    page.generate_page('blog')
    page.generate_page('index')
    page.generate_page('projects')

    post_page = Generator(folder + OUTPUT_POST_FOLDER, folder + 'templates', BASE_URL,
                          posts_metadata, sitemap, site_title=SITE_TITLE,
                          minify_code=minify)

    for post in POSTS:
        post_metadata = POSTS[post].metadata

        post_data = {
            'content': POSTS[post],
            'title': post_metadata['title'],
            'date': post_metadata['date'],
            'author': post_metadata['author']
        }
        os.makedirs(folder + OUTPUT_POST_FOLDER, exist_ok=True)

        post_page.generate_page('{slug}'.format(slug=post_metadata['slug']), template_name='post', post=post_data)

    copy_tree(folder + get_config_setting('build', 'static_folder'), folder + get_config_setting('build', 'output_folder'))
    sitemap.save_sitemap()
    if minify:
        minify_css_js(folder + OUTPUT_FOLDER)

    end_timer = time.perf_counter()
    print(f'[REBUILD] : Rebuild completed in {end_timer - start_time:0.4f} seconds')


def minify_css_js(folder):
    for file in os.listdir(folder):
        if file.endswith(".css"):
            with open(os.path.join(folder, file), 'r') as css_file:
                raw_css = css_file.read()
                with open(os.path.join(folder, file), 'w') as css_file_minified:
                    css_file_minified.write(compress(raw_css))
        if file.endswith(".js"):
            with open(os.path.join(folder, file), 'r') as js_file:
                raw_js = js_file.read()
                with open(os.path.join(folder, file), 'w') as js_file_minified:
                    js_file_minified.write(rjsmin.jsmin(raw_js))


def watch_on_modified(event):
    if 'output' in str(event.src_path):
        pass
    else:
        rebuild(False, folder=WORKING_PATH)


def create_output_folder(dir='', overwrite=False):
    if os.path.exists(dir):
        if not overwrite:
            print('OUTPUT DIRECTORY ALREADY EXISTS!')
            answer = input('Do you want to overwrite? (y/n): ')
            if answer == 'y':
                shutil.rmtree(dir)
                print("OUTPUT DIRECTORY DELETED, CONTINUING..")
                os.makedirs(dir)
        else:
            shutil.rmtree(dir)
            os.makedirs(dir)
    else:
        os.makedirs(dir)


if __name__ == "__main__":
    main()
