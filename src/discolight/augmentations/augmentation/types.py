from abc import ABC, abstractmethod

import numpy as np


def augmentation_list(*args, **kwargs):
    raise ValueError("This typecast must be bound before validation")


class Augmentation(ABC):
    """An image augmentation"""

    _include_in_factory = True

    @staticmethod
    @abstractmethod
    def params():
        """
        Returns a description of the parameters used to initialize this
        augmentation
        """

    @abstractmethod
    def augment(self, img, bboxes):
        """
        Performs the augmentation, returning the image and bounding boxes as a
        tuple.

        The bounding boxes are stored in a n x 5 numpy array, where n is the
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

    def get_img(self, img):
        """Perform the augmentation on an image with no bounding boxes"""
        bboxes = np.zeros((1, 5))
        img, _ = self.augment(img, bboxes)
        return img


class ColorAugmentation(Augmentation):
    """
    An image augmentation that only modifies the image colors, leaving the
    bounding boxes unchanged.

    Implementations of this class should only override the params and
    augment_img methods.
    """
    @staticmethod
    @abstractmethod
    def params():
        raise NotImplementedError

    @abstractmethod
    def augment_img(self, img, bboxes):
        """Performs the augmentation, returning only the image"""

    def augment(self, img, bboxes):
        return self.augment_img(img, bboxes), bboxes
