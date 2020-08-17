"""A dynamic generator for Discolight documentation."""
from jinja2 import Environment, PackageLoader
from .doc import make_all_doc_objects


def markdown_escape_filter(text):
    """Escape special characters in Markdown."""
    return text.replace("\\", "\\\\").replace("`", "\\`").replace(
        "*", "\\*").replace("_", "\\_").replace("{", "\\{").replace(
            "}", "\\}").replace("[", "\\[").replace("]", "\\]").replace(
                "(", "\\(").replace(")", "\\)").replace("#", "\\#").replace(
                    "+", "\\+").replace("-",
                                        "\\-").replace(".", "\\.").replace(
                                            "!", "\\!").replace("|", "\\|")


def firstline_filter(text):
    """Get the first line of a string."""
    return text.split("\n")[0]


def make_discolight_md(doc_objects, doc_template):
    """Render the doc/discolight.md documentation file.

    This file contains complete documentation for all augmentations,
    loaders, and writers.
    """
    discolight_md = doc_template.render(image_root='images/', **doc_objects)

    with open("./doc/discolight.md", "w") as discolight_md_file:

        discolight_md_file.write(discolight_md)


def make_readme_md(doc_objects, readme_template):
    """Render the README.md documentation file."""
    readme_md = readme_template.render(discolight_md_url='doc/discolight.md',
                                       image_root='doc/images/',
                                       **doc_objects)

    with open("./README.md", "w") as readme_md_file:

        readme_md_file.write(readme_md)


def make_longdescription_md(doc_objects, readme_template):
    """Render the longdescription.md documentation file."""
    longdescription_md = readme_template.render(
        discolight_md_url="https://github.com/datature/discolight"
        "/blob/master/doc/discolight.md",
        image_root="https://raw.githubusercontent.com/"
        "datature/discolight/master/doc/images/",
        **doc_objects)

    with open("./longdescription.md", "w") as longdescription_file:

        longdescription_file.write(longdescription_md)


sample_image_path = "./sample_images/rocks.jpg"
sample_annotations_path = "./sample_images/doc-annotations.csv"
output_dir = "./doc/images/"


def main():
    """Render the dynamically generated documentation for Discolight."""
    template_env = Environment(
        loader=PackageLoader('discolight', 'doc_templates'))
    template_env.filters['markdown'] = markdown_escape_filter
    template_env.filters['firstline'] = firstline_filter

    doc_template = template_env.get_template('discolight.md')
    readme_template = template_env.get_template('readme.md')

    doc_objects = make_all_doc_objects(sample_image_path,
                                       sample_annotations_path, output_dir)

    make_discolight_md(doc_objects, doc_template)

    make_readme_md(doc_objects, readme_template)

    make_longdescription_md(doc_objects, readme_template)


if __name__ == "__main__":
    main()
