# Mango
Mango is a static site generator developed specifically for https://simplymozzo.se using the [jinja](https://github.com/pallets/jinja) templating engine.

## Configuration file
A configuration file can be supplied from the root directory of the website. The name of the file should be `mango.ini`

If no configuration file is found or supplied via the `--config` flag, default options will be used. See below for an explanation of all configuration options including there default values.
`

###Configuration options:
####General section
|Option|Default                 |Explanation|
|---------------|---------------|-----------|
|title          |Default site   |Title of the website, to be used inside of templates.|
|content_folder |content        |Folder where all markdown content is stored.   |
|template_folder|templates      |Folder where all templates are stored.   |
|output_folder  |output         |Folder where the generated output is saved.   |
|output_post_folder|output/posts|Folder where the generated markdown files from the content folder is stored.   |
|static_folder|static           |Folder where all static files are stored, such as css, jss, images.   |

####Server section
|Option|Default     |Explanation|
|------|----------- |-----------|
|host  |localhost|IP address to use when running the builtin dev server.  |
|port  |8080     |Port address to use when running the builtin dev server.|


## License
`mango` is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.
