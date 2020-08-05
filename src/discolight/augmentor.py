"""A YAML-based interface for Discolight."""
import os

from tqdm import tqdm
from .augmentations.factory import make_augmentations_factory
from .loaders.annotation.factory import make_annotation_loader_factory
from .loaders.image.factory import make_image_loader_factory
from .writers.annotation.factory import make_annotation_writer_factory
from .writers.image.factory import make_image_writer_factory
from .augmentations.bbox_utilities import bbox_utilities
from .annotations import (annotations_from_numpy_array,
                          annotations_to_numpy_array)


class Augmentor:

    """A class that performs augmentation operations from a query.

    Queries should be parsed and validated with the query module before
    being passed to this class.
    """

    def __init__(self, query):
        """Initialize the augmentor with the given query.

        NOTE: This class assumes that the given query is valid for the
        operation(s) you wish to perform.
        """
        self.augmentation_factory = make_augmentations_factory()

        self.annotation_loader_factory = make_annotation_loader_factory()
        self.image_loader_factory = make_image_loader_factory()

        self.annotation_writer_factory = make_annotation_writer_factory()
        self.image_writer_factory = make_image_writer_factory()

        self.query = query

    def generate(self):
        """Generate image augmentations.

        Generation is configured by the query passed at class construction.
        """
        image_loader_name = self.query["input"]["images"]["loader"]
        image_loader_opts = self.query["input"]["images"]["options"]

        annot_loader_name = self.query["input"]["annotations"]["loader"]
        annot_loader_opts = self.query["input"]["annotations"]["options"]

        with self.image_loader_factory(
                image_loader_name, **image_loader_opts
        ) as image_loader, self.annotation_loader_factory(
                annot_loader_name, **annot_loader_opts) as annotation_loader:
            images = annotation_loader.load_annotated_images(image_loader)

        augmentations = []

        for augmentation in self.query["augmentations"]:

            augmentations.append(
                self.augmentation_factory(augmentation["name"],
                                          **augmentation.get("options", {})))

        def postprocess(img, bboxes):
            if self.query["save-bbox"]:
                return bbox_utilities.draw_rect(img, bboxes, (255, 0, 0))

            return img

        image_writer_name = self.query["output"]["images"]["writer"]
        image_writer_opts = self.query["output"]["images"]["options"]

        annot_writer_name = self.query["output"]["annotations"]["writer"]
        annot_writer_opts = self.query["output"]["annotations"]["options"]

        with self.image_writer_factory(
                image_writer_name, **image_writer_opts
        ) as image_writer, self.annotation_writer_factory(
                annot_writer_name, **annot_writer_opts) as annotation_writer:

            for image_name in tqdm(images, desc="Augmenting...", unit="img"):

                img, annotations = images[image_name]

                height, width, _ = img.shape

                for annotation in annotations:
                    if (annotation.x_min < 0 or annotation.y_min < 0
                            or annotation.x_max < 0 or annotation.y_max < 0):
                        raise ValueError(
                            "Annotation {} for image {} contains negative "
                            "coordinates for the bounding box!".format(
                                annotation, image_name))

                    if annotation.x_min > annotation.x_max:
                        raise ValueError(
                            "Annotation {} for image {} has x_min > x_max!".
                            format(annotation, image_name))

                    if annotation.y_min > annotation.y_max:
                        raise ValueError(
                            "Annotation {} for image {} has y_min > y_max!".
                            format(annotation, image_name))

                    if (annotation.x_min > width or annotation.y_min > height
                            or annotation.x_max > width
                            or annotation.y_max > height):
                        raise ValueError(
                            "Annotation {} for image {} contains coordinates "
                            "for the bounding box that are greater than the "
                            "image dimensions!".format(annotation, image_name))

                annotation_writer.write_annotations_for_image(
                    image_name, img, annotations)

                bboxes = annotations_to_numpy_array(annotations)

                if self.query["save-original"]:
                    image_writer.write_image(image_name,
                                             postprocess(img, bboxes))

                augmentation_idx = 1

                for augmentation in tqdm(augmentations,
                                         desc=image_name,
                                         leave=False,
                                         unit="aug"):
                    image_name_base, ext = os.path.splitext(image_name)
                    augmented_image_name = "{}--{}{}".format(
                        image_name_base, augmentation_idx, ext)

                    aug_img, aug_bboxes = augmentation.augment(
                        img.copy(), bboxes.copy())

                    image_writer.write_image(augmented_image_name,
                                             postprocess(aug_img, aug_bboxes))

                    augmented_annotations = annotations_from_numpy_array(
                        aug_bboxes)

                    annotation_writer.write_annotations_for_image(
                        augmented_image_name, aug_img, augmented_annotations)

                    augmentation_idx += 1
