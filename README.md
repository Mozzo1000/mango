# Mango
Mango is a static site generator developed specifically for https://andreasbackstrom.se using the [jinja](https://github.com/pallets/jinja) templating engine.

## Features
* Automatic sitemap generation
* Supports markdown files for blog-like posts
* Jinja2 templating
* Builtin development web server


## Configuration file
A configuration file can be supplied from the root directory of the website. The name of the file should be `mango.toml`

If no configuration file is found or supplied via the `--config` flag, a file will be created with default options. See below for an explanation of all configuration options including there default values.
`

### Configuration options:
#### General section
|Option|Default                 |Explanation|
|---------------|---------------|-----------|
|title          |Default site   |Title of the website, to be used inside of templates.|
|base_url       |http://example.com   |Url of your website, is used for several things including sitemap generation.|

#### Build section
|Option|Default                 |Explanation|
|---------------|---------------|-----------|
|content_folder |content        |Folder where all markdown content is stored.   |
|template_folder|templates      |Folder where all templates are stored.   |
|output_folder  |output         |Folder where the generated output is saved.   |
|output_post_folder|output/posts|Folder where the generated markdown files from the content folder is stored.   |
|static_folder|static           |Folder where all static files are stored, such as css, jss, images.   |

#### Sitemap section
|Option|Default     |Explanation|
|------|----------- |-----------|
|use_html_extension  |False|Defines if the sitemap generator should append .html to url or not.|


#### Server section
|Option|Default     |Explanation|
|------|----------- |-----------|
|host  |localhost|IP address to use when running the builtin dev server.  |
|port  |8080     |Port address to use when running the builtin dev server.|

## Development
**Python version tested with:** 3.7.3 

|Development dependencies|
|------|
|flake8|
 
### Install development dependencies
To install all development related dependencies, run `pip install -e .[dev]` in the root directory of this project. 
 
### Run linter
We use the flake8 to check for linting errors in our code. Inside tox.ini there is a configuration set that `flake8`
will automatically use.

Just run `flake8` in the root directory to run the linter.

## License
`mango` is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.
