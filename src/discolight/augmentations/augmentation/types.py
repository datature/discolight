"""Base types for image augmentations."""
from abc import ABC, abstractmethod

import numpy as np


def augmentation_list(*args, **kwargs):
    """Cast a value to a list of annotations.

    This type cast can be used by augmentations that take in a list of
    augmentations in their constructors. This type cast will be bound
    to an actual casting function in the augmentation factory.
    """
    raise ValueError("This typecast must be bound before validation")


class Augmentation(ABC):

    """An image augmentation."""

    _include_in_factory = True

    @staticmethod
    @abstractmethod
    def params():
        """Return a Params object describing constructor parameters."""
        raise NotImplementedError

    @abstractmethod
    def augment(self, img, bboxes):
        """Perform the augmentation on an image and its annotations.

        The bounding boxes are passed as a n x 5 numpy array, where n is the
        number of bounding boxes. The columns are as follows:
        0: x_min
        1: x_max
        2: y_min
        3: y_max
        4: label

        Keyword arguments:
        img: An opencv image in HxWxC format
        bboxes: A numpy array containing the bounding boxes for annotations
        """
        raise NotImplementedError

    def get_img(self, img):
        """Perform the augmentation on an image with no bounding boxes."""
        bboxes = np.zeros((1, 5))
        img, _ = self.augment(img, bboxes)
        return img


class ColorAugmentation(Augmentation):

    """An image augmentation that only modifies the image colors.

    ColorAugmentations do not modify image annotations.

    Implementations of this class should only override the params and
    augment_img methods.
    """

    @staticmethod
    @abstractmethod
    def params():
        """Return a Params object describing constructor parameters."""
        raise NotImplementedError

    @abstractmethod
    def augment_img(self, img, bboxes):
        """Perform the augmentation, returning only the augmented image."""

    def augment(self, img, bboxes):
        """Perform the augmentation on an image and its annotations."""
        return self.augment_img(img, bboxes), bboxes
