import xml.etree.cElementTree as ET
from urllib.parse import urlparse
from mango.config import get_config_setting


class Sitemap:
    def __init__(self, location):
        self.location = location
        self.root = ET.Element('urlset')
        self.root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

    def add_sitemap(self, url, modified, change='monthly', priority='0.8'):
        if get_config_setting('sitemap', 'use_html_extension') == "True":
            if not urlparse(url).path == '':
                url = url + '.html'
            if urlparse(url).path == '/index.html':
                url = url.replace('index.html', '')
        if urlparse(url).path == '/index':
            url = url.replace('/index', '')

        doc = ET.SubElement(self.root, 'url')
        ET.SubElement(doc, 'loc').text = url
        ET.SubElement(doc, 'lastmod').text = modified
        ET.SubElement(doc, 'changefreq').text = change
        ET.SubElement(doc, 'priority').text = priority

    def save_sitemap(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.location + '/sitemap.xml', encoding='utf-8', xml_declaration=True)
