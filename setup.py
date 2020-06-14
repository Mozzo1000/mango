import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    for line in read('mango/__init__.py').splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='mango',
    version=get_version(),
    author='Andreas Backström',
    author_email='mozzo242@gmail.com',
    description='A static site generator developed specifically for andreasbackstrom.se',
    license='Apache-2.0',
    keywords='static site generator jinja2 web markdown',
    install_requires=['markdown2', 'jinja2', 'htmlmin',
                      'csscompressor', 'rjsmin', 'watchdog',
                      'toml'],
    extras_require={
        'dev': [
            'flake8'
        ]
    },
    packages=['mango'],
    entry_points={
        'console_scripts': ['mango=mango.main:main'],
    },
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
    ]
)
