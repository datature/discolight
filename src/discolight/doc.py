# flake8: noqa
import inspect
import os
import re
import shutil
import argparse
from tqdm import tqdm
from jinja2 import Environment, BaseLoader
from .augmentations import factory as augmentations_factory
from .loaders.annotation import factory as annotation_loader_factory
from .loaders.image import factory as image_loader_factory
from .writers.annotation import factory as annotation_writer_factory
from .writers.image import factory as image_writer_factory

doc_template_str = """
# Annotation Loaders

{% for annot_ldr in annotation_loaders %}
## {{ annot_ldr.name|markdown }}

{{ annot_ldr.description|markdown }}

### Parameters

{% for parameter in annot_ldr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if annot_ldr.ensures %}
#### Other Conditions


{% for ensure in annot_ldr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Annotation Writers

{% for annot_wtr in annotation_writers %}
## {{ annot_wtr.name|markdown }}

{{ annot_wtr.description|markdown }}

### Parameters

{% for parameter in annot_wtr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if annot_wtr.ensures %}
#### Other Conditions

{% for ensure in annot_wtr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Image Loaders

{% for image_ldr in image_loaders %}
## {{ image_ldr.name|markdown }}

{{ image_ldr.description|markdown }}

### Parameters

{% for parameter in image_ldr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if image_ldr.ensures %}
#### Other Conditions

{% for ensure in image_ldr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Image Writers

{% for image_wtr in image_writers %}
## {{ image_wtr.name|markdown }}

{{ image_wtr.description|markdown }}

### Parameters

{% for parameter in image_wtr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if image_wtr.ensures %}
#### Other Conditions

{% for ensure in image_wtr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Augmentations

{% for augmentation in augmentations %}
## {{ augmentation.name|markdown }}

{{ augmentation.description|markdown }}

### Example
<table>
<tr>
<td style="vertical-align: bottom">
<img src="{{ augmentation.sample_image }}"/>
<br/>
Input Image
</td>
<td style="vertical-align: bottom">
<img src="{{ augmentation.augmented_image }}" />
<br/>
Augmented Image
</td>
</tr>
</table>

### Parameters

{% for parameter in augmentation.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if augmentation.ensures %}
#### Other Conditions

{% for ensure in augmentation.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}
"""


def markdown_escape_filter(text):
    """A jinja2 filter that will escape special characters in Markdown"""
    return text.replace("\\", "\\\\").replace("`", "\\`").replace(
        "*", "\\*").replace("_", "\\_").replace("{", "\\{").replace(
            "}", "\\}").replace("[", "\\[").replace("]", "\\]").replace(
                "(", "\\(").replace(")", "\\)").replace("#", "\\#").replace(
                    "+", "\\+").replace("-",
                                        "\\-").replace(".", "\\.").replace(
                                            "!", "\\!").replace("|", "\\|")


template_env = Environment(loader=BaseLoader())
template_env.filters['markdown'] = markdown_escape_filter

doc_template = template_env.from_string(doc_template_str)

augmentation_fy = augmentations_factory.make_augmentations_factory()

annotation_ldr_fy = annotation_loader_factory.make_annotation_loader_factory()
annotation_wtr_fy = annotation_writer_factory.make_annotation_writer_factory()

image_loader_fy = image_loader_factory.make_image_loader_factory()
image_writer_fy = image_writer_factory.make_image_writer_factory()


def make_doc_object(obj):
    """
    Takes an object with a docstring and params and generates a dictionary
    object that will be fed to the template used to generate documentation.
    """
    doc_object = {}

    doc_object["name"] = obj.__name__

    doc_string = obj.__doc__ if obj.__doc__ is not None else ""

    doc_object["description"] = inspect.cleandoc(doc_string)

    parameters = {}

    for param in obj.params().params.values():

        param_doc_object = {
            "name": param["name"],
            "description": param["description"],
            "type": param["data_type"].__name__,
            "default": str(param["default"]),
            "required": param["required"],
            "ensures": []
        }

        parameters[param["name"]] = param_doc_object

    doc_object["ensures"] = []

    for ensure in obj.params().ensures:

        found_matching_parameter = False

        for param in parameters:

            # First look for validation conditions that start with the
            # parameter name. We will pull out the rest of this string and
            # put it under that parameter in the final product.
            match = re.search('^{} (.*)'.format(param), ensure["err"])

            if match is not None:
                parameters[param]["ensures"].append(match.group(1))
                found_matching_parameter = True
                continue

            match = re.search(param, ensure["err"])

            # If we find a match somwhere else we include the entire string
            # under that parameter in the final product.
            if match is not None:
                parameters[param]["ensures"].append(ensure["err"])
                found_matching_parameter = True
                continue

        if not found_matching_parameter:
            doc_object["ensures"].append(ensure["err"])

    doc_object["parameters"] = list(parameters.values())
    doc_object["parameters"].sort(key=lambda pdo: pdo["name"])

    return doc_object


def make_augmentation_doc_object(augmentation, sample_image_path, output_dir,
                                 image_root):
    """
    Takes an augmentation class and generates a dictionary object that will be
    fed to the template used to generate documentation.
    """

    doc_object = make_doc_object(augmentation)

    augmentation_instance = augmentation_fy(augmentation.__name__)

    with image_loader_fy(
            'Directory',
            directory=os.path.dirname(sample_image_path)) as image_loader:
        image = image_loader.load_image(os.path.basename(sample_image_path))

    sample_image_path = os.path.join(
        output_dir, "{}-input.jpg".format(augmentation.__name__))

    with image_writer_fy('Directory',
                         directory=output_dir,
                         clean_directory=False) as image_writer:
        image_writer.write_image("{}-input.jpg".format(augmentation.__name__),
                                 image)

        augmented_image = augmentation_instance.get_img(image)

        image_writer.write_image("{}.jpg".format(augmentation.__name__),
                                 augmented_image)

    doc_object["sample_image"] = os.path.join(
        image_root, "{}-input.jpg".format(augmentation.__name__))
    doc_object["augmented_image"] = os.path.join(
        image_root, "{}.jpg".format(augmentation.__name__))

    return doc_object


def document(sample_image_path, output_dir, image_root):

    annotation_ldrs_set = annotation_loader_factory.get_annotation_loader_set()
    annotation_wtrs_set = annotation_writer_factory.get_annotation_writer_set()
    image_ldrs_set = image_loader_factory.get_image_loader_set()
    image_wtrs_set = image_writer_factory.get_image_writer_set()
    augmentations_set = augmentations_factory.get_augmentations_set()

    annotation_loaders_list = []
    annotation_writers_list = []
    image_loaders_list = []
    image_writers_list = []
    augmentations_list = []

    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

        os.mkdir(output_dir)

    for annot_ldr in tqdm(annotation_ldrs_set.values(),
                          desc="Annotation Loaders",
                          unit="ldr"):
        annotation_loaders_list.append(make_doc_object(annot_ldr))

    for annot_wtr in tqdm(annotation_wtrs_set.values(),
                          desc="Annotation Writers",
                          unit="ldr"):
        annotation_writers_list.append(make_doc_object(annot_wtr))

    for image_ldr in tqdm(image_ldrs_set.values(),
                          desc="Image Loaders",
                          unit="ldr"):
        image_loaders_list.append(make_doc_object(image_ldr))

    for image_wtr in tqdm(image_wtrs_set.values(),
                          desc="Image Writers",
                          unit="ldr"):
        image_writers_list.append(make_doc_object(image_wtr))

    for augmentation in tqdm(augmentations_set.values(),
                             desc="Augmentations",
                             unit="aug"):
        augmentations_list.append(
            make_augmentation_doc_object(augmentation, sample_image_path,
                                         output_dir, image_root))

    annotation_loaders_list.sort(key=lambda do: do["name"])
    annotation_writers_list.sort(key=lambda do: do["name"])
    image_loaders_list.sort(key=lambda do: do["name"])
    image_writers_list.sort(key=lambda do: do["name"])

    augmentations_list.sort(key=lambda ado: ado["name"])

    print(
        doc_template.render(augmentations=augmentations_list,
                            annotation_loaders=annotation_loaders_list,
                            annotation_writers=annotation_writers_list,
                            image_loaders=image_loaders_list,
                            image_writers=image_writers_list))


def main():

    parser = argparse.ArgumentParser(
        description='Generate Discolight documentation')

    parser.add_argument('--sample-image',
                        dest='sample_image_path',
                        default=['./sample_images/wheat1.jpg'],
                        nargs=1)
    parser.add_argument('--output-dir',
                        dest='output_dir',
                        default=['./doc/images'],
                        nargs=1)
    parser.add_argument('--image-root',
                        dest='image_root',
                        default=['images/'],
                        nargs=1)

    args = parser.parse_args()

    document(args.sample_image_path[0], args.output_dir[0], args.image_root[0])


if __name__ == "__main__":
    main()
