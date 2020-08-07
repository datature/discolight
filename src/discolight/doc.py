"""A documentation generator for loaders, writers, and augmentations."""
import csv
import inspect
import os
import random
import re
import shutil
from enum import Enum
import yamale
import yaml
from tqdm import tqdm
from .annotations import (BoundingBox, annotations_from_numpy_array,
                          annotations_to_numpy_array)
from .util.image import load_image, save_image
from .augmentations import factory as augmentations_factory
from .loaders.annotation import factory as annotation_loader_factory
from .loaders.image import factory as image_loader_factory
from .writers.annotation import factory as annotation_writer_factory
from .writers.image import factory as image_writer_factory
from .doc_templates import augmentations as augmentation_options

augmentation_fy = augmentations_factory.make_augmentations_factory()

annotation_ldr_fy = annotation_loader_factory.make_annotation_loader_factory()
annotation_wtr_fy = annotation_writer_factory.make_annotation_writer_factory()

image_loader_fy = image_loader_factory.make_image_loader_factory()
image_writer_fy = image_writer_factory.make_image_writer_factory()


def hr_type_name(typ):
    """Get a human-readable representation of a type."""
    try:
        if issubclass(typ, Enum):
            return " | ".join([v.value for v in typ])
    except TypeError:
        pass

    if hasattr(typ, "__name__"):

        return typ.__name__

    return str(typ)


def make_doc_object(obj):
    """Generate a description of an object for use in a template."""
    doc_object = {}

    doc_object["name"] = obj.__name__

    doc_string = obj.__doc__ if obj.__doc__ is not None else ""

    doc_object["description"] = inspect.cleandoc(doc_string)

    parameters = {}

    for param in obj.params().params.values():

        param_doc_object = {
            "name": param["name"],
            "description": param["description"],
            "type": hr_type_name(param["data_type"]),
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


def load_annotations_for_sample_image(annotations_path):
    """Load annotations for the sample image from a CSV file.

    The CSV file should have the following format:

    x_min, y_min, x_max, y_max, label
    ...
    """
    annotations = []

    with open(annotations_path, newline='') as csv_file:

        reader = csv.DictReader(csv_file, skipinitialspace=True)

        for row in reader:

            annotations.append(
                BoundingBox(float(row['x_min']), float(row['y_min']),
                            float(row['x_max']), float(row['y_max']),
                            int(row['label'])))

    return annotations


def make_augmentation_doc_object(augmentation, sample_image_path,
                                 sample_annotations_path, output_dir):
    """Generate an object for documenting an augmentation in a template.

    This function invokes make_doc_object, and augments the returned
    document object by augmenting a sample image from sample_image_path.
    The augmented image will be stored in output_dir, and referenced in
    the template as being inside image_root.
    """
    doc_object = make_doc_object(augmentation)

    options_dir = os.path.dirname(augmentation_options.__file__)

    options = {}
    try:
        with open(
                os.path.join(options_dir, "{}.yml".format(
                    augmentation.__name__))) as options_file:
            content = options_file.read()

            options = yamale.make_data(content=content)[0][0]
    except IOError:
        pass

    if options != {}:
        doc_object["sample_options"] = yaml.dump(options,
                                                 default_flow_style=False)

    random.seed(1)
    augmentation_instance = augmentation_fy(augmentation.__name__, **options)

    image = load_image(sample_image_path)
    annotations = load_annotations_for_sample_image(sample_annotations_path)

    annotations = list(
        map(lambda bbox: bbox.unnormalize(image.shape[1], image.shape[0]),
            annotations))

    sample_image_path = os.path.join(
        output_dir, "{}-input.jpg".format(augmentation.__name__))

    save_image(
        os.path.join(output_dir, "{}-input.jpg".format(augmentation.__name__)),
        image)
    save_image(
        os.path.join(output_dir,
                     "{}-input-bboxes.jpg".format(augmentation.__name__)),
        image, annotations, (0, 255, 0), 15)

    bboxes = annotations_to_numpy_array(annotations)

    augmented_image, augmented_bboxes = augmentation_instance.augment(
        image, bboxes)

    augmented_annotations = annotations_from_numpy_array(augmented_bboxes)

    save_image(
        os.path.join(output_dir, "{}.jpg".format(augmentation.__name__)),
        augmented_image)
    save_image(
        os.path.join(output_dir,
                     "{}-bboxes.jpg".format(augmentation.__name__)),
        augmented_image, augmented_annotations, (0, 255, 0), 15)

    doc_object["sample_image"] = "{}-input.jpg".format(augmentation.__name__)
    doc_object["sample_image_bboxes"] = "{}-input-bboxes.jpg".format(
        augmentation.__name__)
    doc_object["augmented_image"] = "{}.jpg".format(augmentation.__name__)
    doc_object["augmented_image_bboxes"] = "{}-bboxes.jpg".format(
        augmentation.__name__)

    return doc_object


def make_all_doc_objects(sample_image_path, sample_annotations_path,
                         output_dir):
    """Produce documentation objects for loaders, writers, and annotations.

    The doc objects are returned in dictionary that can be passed to a
    template.

    The image in sample_image_path will be used to showcase installed
    augmentations. Augmented images will be stored in output_dir, and
    referenced within the finished documentation as being in
    image_root.
    """
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
                                         sample_annotations_path, output_dir))

    annotation_loaders_list.sort(key=lambda do: do["name"])
    annotation_writers_list.sort(key=lambda do: do["name"])
    image_loaders_list.sort(key=lambda do: do["name"])
    image_writers_list.sort(key=lambda do: do["name"])

    augmentations_list.sort(key=lambda ado: ado["name"])

    return {
        "augmentations": augmentations_list,
        "annotation_loaders": annotation_loaders_list,
        "annotation_writers": annotation_writers_list,
        "image_loaders": image_loaders_list,
        "image_writers": image_writers_list
    }
