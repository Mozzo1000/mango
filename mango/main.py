from argparse import ArgumentParser
import markdown2
import os
import shutil
import json
import sys
from config import get_config_setting, generate_config, check_config_exists
from defaults import create_default_files
from http.server import HTTPServer
from httpserver import SimpleServer


def main():
    global head_file
    global foot_file

    parser = ArgumentParser(description='')
    parser.add_argument('--file', help='Input file')
    parser.add_argument('--layout', help='Layout file')
    parser.add_argument('--config', help='Config file')
    parser.add_argument('--generate-config', help='Generate config file', action='store_true')
    parser.add_argument('--create-project', help='Create a default project folder structure')
    parser.add_argument('--server', help='Run a development server', action='store_true')

    if parser.parse_args().create_project:
        project_name = parser.parse_args().create_project
        if os.path.exists(project_name):
            print('Folder already exists, please use a non existing folder.')
        else:
            os.makedirs(project_name)
            os.makedirs(project_name + '/include')
            os.makedirs(project_name + '/partials')
            os.makedirs(project_name + '/layouts')
            os.makedirs(project_name + '/posts')
            generate_config('partials/header.html', 'layouts/default.html', 'partials/footer.html', location=project_name + '/')
            create_default_files(project_name)
    elif parser.parse_args().generate_config:
            generate_config('', '', '')
    elif parser.parse_args().server:
        try:
            server = HTTPServer(('localhost', 8080), SimpleServer)
            print('Running web server on http://localhost:8080 (Press CTRL+C to quit)')
            server.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down the web server')
            sys.exit()
            server.socket.close()
    else:
        if os.path.exists('output'):
            print('OUTPUT DIRECTORY ALREADY EXISTS!')
            answer = input('Do you want to overwrite? (y/n): ')
            if answer == 'y':
                shutil.rmtree('output')
                print("OUTPUT DIRECTORY DELETED, CONTINUING..")
                os.makedirs('output')
                if not os.path.exists('output/posts'):
                    os.makedirs('output/posts')
        else:
            os.makedirs('output')
            if not os.path.exists('output/posts'):
                os.makedirs('output/posts')

        if check_config_exists and parser.parse_args().config is None:
            head_file = get_config_setting('partials', 'header')
            foot_file = get_config_setting('partials', 'footer')
            layout_file = get_config_setting('layout', 'default')
        elif parser.parse_args().config:
            config_file = parser.parse_args().config
            head_file = get_config_setting('partials', 'header', file_override=config_file)
            foot_file = get_config_setting('partials', 'footer', file_override=config_file)
            layout_file = get_config_setting('layout', 'default', file_override=config_file)

        else:
            print('Error: No head or layout file has been supplied.')

        if parser.parse_args().file:
            file = open(parser.parse_args().file, 'r')
            html = markdown2.markdown(file.read(), extras=["metadata"])
            file.close()

            if 'layout' in html.metadata:
                add(html.metadata['layout'], html, parser.parse_args().file.replace('.md', '.html'))
            else:
                add(layout_file, html, parser.parse_args().file.replace('.md', '.html'))


def add(workfile, html, output):
    with open(workfile, 'r') as file:
        file_input = file.read()

    if os.path.dirname(output):
        go_back_var = 1
    else:
        go_back_var = 0

    after_head = insert_head(file_input, go_back_var)
    after_body = insert_content(after_head, html)
    after_footer = insert_footer(after_body)

    if 'posts' in output:
        if not os.path.isfile('.all_posts.json'):
            with open('.all_posts.json', mode='w') as f:
                f.write(json.dumps({'all_posts': []}, indent=2))
        with open('.all_posts.json', 'r') as json_file:
            existing_json_file = json.load(json_file)
            already_exists = False
            for item in existing_json_file['all_posts']:
                if output in item['file']:
                    print('exists ' + str(output))
                    already_exists = True

            if not already_exists:
                existing_json_file['all_posts'].append({'file': output, 'title': html.metadata['title']})
                with open('.all_posts.json', mode='w') as f:
                     f.write(json.dumps(existing_json_file, indent=2))

    output_file = open('output/' + output, 'w+')
    output_file.write(after_footer)
    output_file.close()

    copytree('include', 'output')


def insert_head(file_input, go_back_var):
    go_back_var_replace = ''
    if go_back_var >= 1:
        go_back_var_replace = '../'
    with open(head_file, 'r') as head:
        file_input = file_input.replace('[[HEAD]]', head.read()).replace('[[DIR]]', go_back_var_replace)
    return file_input


def insert_footer(file_input):
    with open(foot_file, 'r') as foot:
        file_input = file_input.replace('[[FOOTER]]', foot.read())
    return file_input


def insert_content(file_input, html):
    file_input = file_input.replace('[[CONTENT]]', html).replace('[[TITLE]]', html.metadata['title'])\
        .replace('[[ALLPOSTS]]', 'NOT IMPLEMENTED')
    return file_input


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
