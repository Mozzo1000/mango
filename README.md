# Mango
Mango is a static site generator developed specifically for https://simplymozzo.se

## Template specification
### Partials
A partial file is an html file that can be inserted into a layout file or markdown file.

### Layouts
A layout file is how the basic structure of a page is defined.

### Folders explanation
#### include
Everything inside a folder named `include` and is residing in the root directory of your project folder will be copied 
over to the output directory in it's entirety.
#### partials

#### layouts

#### Default project folder structure
* include
* partials
  * header.html
  * footer.html
* layouts
  * default.html
* mango.ini

### Syntax
`[[HEAD]]` = Insert head file.

`[[FOOTER]]` = Insert footer file.

`[[CONTENT]]` = Insert markdown content

`[[TITLE]]` = Insert title metadata from markdown file

`[[DIR]]` = Indicated that the following string is pointing to a directory, used to get correct path even if the
source file is in root or in posts.

## Configuration file
A configuration file can be supplied from the root directory of the website. The name of the file should be `mango.ini`

## License
`mango` is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.
