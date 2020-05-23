from argparse import ArgumentParser
import markdown2
import os
import shutil
import sys
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from defaults import create_default_files
from http.server import HTTPServer
from httpserver import SimpleServer

CONTENT_FOLDER = 'content'
TEMPLATE_FOLDER = 'templates'
OUTPUT_FOLDER = 'output'
STATIC_FOLDER = 'static'
OUTPUT_POST_FOLDER = OUTPUT_FOLDER + '/posts'


def main():
    parser = ArgumentParser(description='')
    parser.add_argument('path', default='')
    parser.add_argument('--create-project', help='Create a default project folder structure')
    parser.add_argument('--server', help='Run a development server', action='store_true')
    parser.add_argument('--rebuild', help='Rebuilds all files', action='store_true')

    if parser.parse_args().path:
        print('PATH SUPPLIED: ' + parser.parse_args().path)

    if parser.parse_args().rebuild:
        rebuild(folder=parser.parse_args().path)
    elif parser.parse_args().create_project:
        project_name = parser.parse_args().create_project
        if os.path.exists(project_name):
            print('Folder already exists, please use a non existing folder.')
        else:
            os.makedirs(project_name)
            os.makedirs(project_name + '/content')
            os.makedirs(project_name + '/static')
            os.makedirs(project_name + '/templates')
            create_default_files(project_name)
    elif parser.parse_args().server:
        try:
            server = HTTPServer(('localhost', 8080), SimpleServer)
            print('Running web server on http://localhost:8080 (Press CTRL+C to quit)')
            server.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down the web server')
            sys.exit()
            server.socket.close()


def rebuild(folder=''):
    POSTS = {}

    for markdown_post in os.listdir(folder + CONTENT_FOLDER):
        file_path = os.path.join(folder + CONTENT_FOLDER, markdown_post)

        with open(file_path, 'r') as file:
            POSTS[markdown_post] = markdown2.markdown(file.read(), extras=['metadata'])

    POSTS = {
        post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
    }

    create_output_folder(base_dir=folder, overwrite=True)

    env = Environment(loader=FileSystemLoader(folder + 'templates'))
    blog_template = env.get_template('blog.html')
    post_template = env.get_template('post.html')
    index_template = env.get_template('index.html')
    projects_template = env.get_template('projects.html')

    posts_metadata = [POSTS[post].metadata for post in POSTS]
    blog_html = blog_template.render(posts=posts_metadata)
    with open(folder + OUTPUT_FOLDER + '/blog.html', 'w') as file:
        file.write(blog_html)
    index_html = index_template.render()
    with open(folder + OUTPUT_FOLDER + '/index.html', 'w') as file:
        file.write(index_html)
    projects_html = projects_template.render()
    with open(folder + OUTPUT_FOLDER + '/projects.html', 'w') as file:
        file.write(projects_html)

    for post in POSTS:
        post_metadata = POSTS[post].metadata

        post_data = {
            'content': POSTS[post],
            'title': post_metadata['title'],
            'date': post_metadata['date'],
            'author': post_metadata['author']
        }

        post_html = post_template.render(post=post_data)
        post_file_path = folder + OUTPUT_POST_FOLDER + '/{slug}.html'.format(slug=post_metadata['slug'])

        print(os.path.dirname(post_file_path))
        os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
        with open(post_file_path, 'w') as file:
            file.write(post_html)

    copytree(folder + STATIC_FOLDER, folder + OUTPUT_FOLDER)


def create_output_folder(base_dir='', overwrite=False):
    if os.path.exists(base_dir + OUTPUT_FOLDER):
        if not overwrite:
            print('OUTPUT DIRECTORY ALREADY EXISTS!')
            answer = input('Do you want to overwrite? (y/n): ')
            if answer == 'y':
                shutil.rmtree(base_dir + OUTPUT_FOLDER)
                print("OUTPUT DIRECTORY DELETED, CONTINUING..")
                os.makedirs(base_dir + OUTPUT_FOLDER)
        else:
            shutil.rmtree(base_dir + OUTPUT_FOLDER)
            print("OUTPUT DIRECTORY DELETED, CONTINUING..")
            os.makedirs(base_dir + OUTPUT_FOLDER)
    else:
        os.makedirs(base_dir + OUTPUT_FOLDER)


def copytree(src, dst, symlinks=False, ignore=None):
    try:
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
    except FileExistsError:
        pass


if __name__ == "__main__":
    main()
