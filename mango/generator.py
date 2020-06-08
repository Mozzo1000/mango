import htmlmin
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


class Generator:
    def __init__(self, output_folder, template_folder, url, metadata, sitemap, site_title='Default site', minify_code=False):
        self.output_folder = output_folder
        self.template_folder = template_folder
        self.url = url
        self.metadata = metadata
        self.sitemap = sitemap
        self.site_title = site_title
        self.minify_code = minify_code

        self.env = Environment(loader=FileSystemLoader(self.template_folder))
        self.current_date = str(datetime.date(datetime.now()))

    def generate_page(self, name, template_name=None, **render):
        template = self.env.get_template((name if template_name is None else template_name) + '.html')
        html = template.render(render, posts=self.metadata, title=self.site_title)
        with open(self.output_folder + '/' + name + '.html', 'w') as file:
            if self.minify_code:
                html = htmlmin.minify(html, remove_empty_space=True)
            file.write(html)
            self.sitemap.add_sitemap(self.url + '/' + name, self.current_date, change='weekly')



