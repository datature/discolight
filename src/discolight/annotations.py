"""A module providing helper functions for handling annotations."""
from collections import namedtuple
import numpy as np


class BoundingBox:

    """A bounding box for an image annotation."""

    def __init__(self, x_min, y_min, x_max, y_max, class_idx):
        """Construct a new bonding box object."""
        self.x_min = float(x_min)
        self.y_min = float(y_min)
        self.x_max = float(x_max)
        self.y_max = float(y_max)
        self.class_idx = int(class_idx)

    def __str__(self):
        """Return a string representation of the bounding box."""
        return "class {} @ (x_min={}, y_min={}, x_max={}, y_max={})".format(
            self.class_idx, self.x_min, self.y_min, self.x_max, self.y_max)

    def normalize(self, width, height):
        """Return a new bounding box with normalized coordinates."""
        return BoundingBox(self.x_min / width, self.y_min / height,
                           self.x_max / width, self.y_max / height,
                           self.class_idx)

    def unnormalize(self, width, height):
        """Return a new bounding box with unnormalized coordinates."""
        return BoundingBox(self.x_min * width, self.y_min * height,
                           self.x_max * width, self.y_max * height,
                           self.class_idx)

    def as_list(self):
        """Return the bounding box coordinates and class ID as a list.

        This makes it easier to generate the bounding box data passed to the
        augmentations in numpy array format.
        """
        return [self.x_min, self.y_min, self.x_max, self.y_max, self.class_idx]


ImageWithAnnotations = namedtuple('ImageWithAnnotations', 'image bboxes')


def annotations_to_numpy_array(bboxes):
    """Convert a list of BoundingBox objects to a numpy array.

    Image augmenations expect annotations to be passed in unnormalized
    format in a numpy array.
    """
    bbox_list = list(map(lambda bbox_object: bbox_object.as_list(), bboxes))

    return np.array(bbox_list).reshape(-1, 5)


def annotations_from_numpy_array(bboxes):
    """Convert an annotation numpy array into a list of BoundingBox objects.

    The bounding boxes returned will be in unnormalized format.
    """
    return list(map(lambda fields: BoundingBox(*fields), bboxes))
