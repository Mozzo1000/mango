default_index = '''
    {% extends "layout.html" %}

    {% block content %}
        <p>Default index</p>
    {% endblock %}
'''

default_layout = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>default project title</title>
        </head>
        <body>
            {% block content %} {% endblock %}
        </body>
        <footer>
            <pMade with mango>
        </footer>
    </html>
'''

default_post = '''
---
title: Default title
date: 2020-04-05
slug: default-post
---

This is the default post.
'''


def create_default_files(location):
    with open(location + '/templates/index.html', 'w') as index_file:
        index_file.write(default_index)
    with open(location + '/templates/layout.html', 'w') as layout_file:
        layout_file.write(default_layout)
    with open(location + '/content/default-post.md', 'w') as post_file:
        post_file.write(default_post)
