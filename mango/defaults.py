

default_header = '''
    <head>
        <title>[[TITLE]]</title>
    </head>
'''

default_footer = '''
    <footer>
        <p>Made with mango</p>
    </footer>
'''

default_layout = '''
    <!DOCTYPE html>
    <html>
        [[HEAD]]
        <body>
            [[CONTENT]]
        </body>
    [[FOOTER]]
    </html>
'''

default_post = '''
---
title: Default title
date: 2020-04-05
---

This is the default post.
'''


def create_default_files(location):
    with open(location + '/partials/header.html', 'w') as head_file:
        head_file.write(default_header)
    with open(location + '/partials/footer.html', 'w') as foot_file:
        foot_file.write(default_footer)
    with open(location + '/layouts/default.html', 'w') as layout_file:
        layout_file.write(default_layout)
    with open(location + '/posts/posts-01.md', 'w') as post_file:
        post_file.write(default_post)
