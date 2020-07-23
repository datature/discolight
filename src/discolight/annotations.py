from collections import namedtuple
import numpy as np


class BoundingBox:
    """A bounding box for an image annotation"""
    def __init__(self, x_min, y_min, x_max, y_max, class_idx):

        self.x_min = float(x_min)
        self.y_min = float(y_min)
        self.x_max = float(x_max)
        self.y_max = float(y_max)
        self.class_idx = int(class_idx)

    def __str__(self):
        return "class {} @ (x_min={}, y_min={}, x_max={}, y_max={})".format(
            self.class_idx, self.x_min, self.y_min, self.x_max, self.y_max)

    def normalize(self, width, height):
        """
        Normalizes the bounding box coordinates given the width and height of
        the corresponding image
        """

        return BoundingBox(self.x_min / width, self.y_min / height,
                           self.x_max / width, self.y_max / height,
                           self.class_idx)

    def unnormalize(self, width, height):
        """
        Unnormlizes the bounding box coordinates given the width and height of
        the corresponding image
        """

        return BoundingBox(self.x_min * width, self.y_min * height,
                           self.x_max * width, self.y_max * height,
                           self.class_idx)

    def as_list(self):
        """
        Returns the bounding box coordinates and class ID as a list

        This makes it easier to generate the bounding box data passed to the
        augmentations in numpy array format.
        """
        return [self.x_min, self.y_min, self.x_max, self.y_max, self.class_idx]


ImageWithAnnotations = namedtuple('ImageWithAnnotations', 'image bboxes')


def annotations_to_numpy_array(bboxes):
    """
    converts a list of BoundingBox objects storing annotation information into
    the numpy array format used by augmentations
    """
    bbox_list = list(map(lambda bbox_object: bbox_object.as_list(), bboxes))

    return np.array(bbox_list).reshape(-1, 5)


def annotations_from_numpy_array(bboxes):
    """
    converts annotations stored as a numpy array into a list of BoundingBox
    objects
    """
    return list(map(lambda fields: BoundingBox(*fields), bboxes))
