from argparse import ArgumentParser
import markdown2
import os
import shutil
import time
import rjsmin
from csscompressor import compress
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from distutils.dir_util import copy_tree
from mango.defaults import create_default_files
from mango.config import get_config_setting, generate_config, check_config_exists, set_config_file, get_config_file
from mango.httpserver import WebServer
from mango.sitemap import Sitemap
from mango.generator import Generator

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
    parser.add_argument('--verbose', help='Show verbose output', action='store_true')

    global WORKING_PATH

    if parser.parse_args().path:
        working_path = parser.parse_args().path
        if parser.parse_args().path is '.':
            working_path = os.getcwd() + '/'
        print('PATH SUPPLIED: ' + working_path)
        WORKING_PATH = working_path

    if parser.parse_args().config:
        print(parser.parse_args().config)
        set_config_file(parser.parse_args().config)
    elif check_config_exists(location=working_path):
        if check_config_exists(location=working_path) == 'OTHER_DIR':
            set_config_file(working_path + 'mango.toml')
    else:
        print('No config file found, creating default config file.')
        generate_config(working_path)

    if parser.parse_args().rebuild:
        rebuild(True if parser.parse_args().minify is True else False, folder=working_path,
                verbose=parser.parse_args().verbose)
    elif parser.parse_args().create_project:
        project_name = parser.parse_args().create_project
        if os.path.exists(project_name):
            print('Folder already exists, please use a non existing folder.')
        else:
            os.makedirs(project_name)
            os.makedirs(project_name + '/content')
            os.makedirs(project_name + '/static')
            os.makedirs(project_name + '/templates')
            generate_config(location=project_name + '/')
            create_default_files(project_name)
    elif parser.parse_args().generate_config:
        generate_config('')

    if parser.parse_args().server and parser.parse_args().watch:
        try:
            server = WebServer(str(get_config_setting('server', 'host')), str(get_config_setting('server', 'port')))
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
            server = WebServer(str(get_config_setting('server', 'host')), str(get_config_setting('server', 'port')))
            server.start_server()
        except KeyboardInterrupt:
            server.stop_server()
    if parser.parse_args().watch:
        try:
            event_handler = PatternMatchingEventHandler(patterns='*', ignore_patterns=['output/*'],
                                                        ignore_directories=True)
            event_handler.on_modified = watch_on_modified
            observer = Observer()
            observer.schedule(event_handler, working_path, recursive=True)
            observer.start()
            print('[WATCHER] Started watcher')
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


def rebuild(minify, folder='', verbose=False):
    start_time = time.perf_counter()
    POSTS = {}

    sitemap = Sitemap(folder + get_config_setting('build', 'output_folder'))

    for markdown_post in os.listdir(folder + get_config_setting('build', 'content_folder')):
        if markdown_post.endswith('.md'):
            file_path = os.path.join(folder + get_config_setting('build', 'content_folder'), markdown_post)
            with open(file_path, 'r') as file:
                POSTS[markdown_post] = markdown2.markdown(file.read(), extras=['metadata', 'cuddled-lists'])

    POSTS = {
        post: POSTS[post] for post in sorted(POSTS,
                                             key=lambda post: datetime.strptime(POSTS[post].metadata['date'],
                                                                                '%Y-%m-%d'), reverse=True)
    }
    create_output_folder(dir=folder + get_config_setting('build', 'output_folder'), overwrite=True)

    posts_metadata = [POSTS[post].metadata for post in POSTS]

    page = Generator(folder + get_config_setting('build', 'output_folder'), folder + 'templates',
                     get_config_setting('general', 'base_url'), posts_metadata, sitemap,
                     site_title=get_config_setting('general', 'title'), minify_code=minify)

    for html_files in os.listdir(folder + get_config_setting('build', 'template_folder')):
        if html_files.endswith('.html') and html_files not in get_config_setting('build', 'ignore_files'):
            if verbose:
                print(f'[BUILD] Compiling {html_files}')
            page.generate_page(html_files.replace('.html', ''))

    post_page = Generator(folder + get_config_setting('build', 'output_post_folder'), folder + 'templates',
                          get_config_setting('general', 'base_url'), posts_metadata, sitemap,
                          site_title=get_config_setting('general', 'title'), minify_code=minify)

    for post in POSTS:
        post_metadata = POSTS[post].metadata

        post_data = {
            'content': POSTS[post],
            'title': post_metadata['title'],
            'date': post_metadata['date'],
            'author': post_metadata['author']
        }
        os.makedirs(folder + get_config_setting('build', 'output_post_folder'), exist_ok=True)
        if verbose:
            print(f'[BUILD] Compiling {post}')
        post_page.generate_page('{slug}'.format(slug=post_metadata['slug']), template_name='post', post=post_data)

    copy_tree(folder + get_config_setting('build', 'static_folder'),
              folder + get_config_setting('build', 'output_folder'))
    sitemap.save_sitemap()
    if minify:
        minify_css_js(folder + get_config_setting('build', 'output_folder'))

    end_timer = time.perf_counter()
    print(f'[REBUILD] Rebuild completed in {end_timer - start_time:0.4f} seconds')


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
