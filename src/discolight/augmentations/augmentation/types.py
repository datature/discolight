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


class BoundedNumber:

    """A type cast for a float or int within a certain range."""

    def __init__(self, number_type, minimum=None, maximum=None):
        """Construct a BoundedNumber type cast."""
        self.number_type = number_type
        self.minimum = minimum
        self.maximum = maximum

        minimum_str = "-Inf" if minimum is None else str(minimum)
        maximum_str = "Inf" if maximum is None else str(maximum)

        self.range_str = "[{}, {}]".format(minimum_str, maximum_str)

        self.__name__ = "{} in range {}".format(number_type.__name__,
                                                self.range_str)

    def __call__(self, val):
        """Cast a value to a float within range."""
        val = self.number_type(val)

        if self.minimum is not None and val < self.minimum:
            raise ValueError("{} not in range {}".format(val, self.range_str))

        if self.maximum is not None and val > self.maximum:
            raise ValueError("{} not in range {}".format(val, self.range_str))

        return val


class NumericalRange:

    """A type cast for a numerical range expressed as a tuple.

    Instances of this class can be called as a type cast numerical
    ranges of the forms:

    (min, max)
    [min, max]

    into the 2-tuple (min, max). An exception will be raised if
    min or max cannot be coerced to float values, or if min > max.

    Additionally, an absolute floor and ceiling for min and max
    can be set in the constructor when instantiating this class.
    """

    def __init__(self, minimum=None, maximum=None):
        """Construct a NumericalRange type cast.

        If minimum or maximum are not None, an exception will be
        raised during casting if min or max in the given numberical
        range (min, max) are not in the interval [minimum, maximum].
        """
        self.minimum = minimum
        self.maximum = maximum

        range_min_str = "-Inf" if minimum is None else str(minimum)
        range_max_str = "Inf" if maximum is None else str(maximum)
        self.__name__ = "range in [{}, {}]".format(range_min_str,
                                                   range_max_str)

    def __call__(self, numerical_range):
        """Cast a value to a numerical range tuple."""
        try:
            numerical_range_tuple = tuple(numerical_range)
        except TypeError:
            raise ValueError("Cannot convert {} to 2-tuple".format(
                repr(numerical_range)))

        if len(numerical_range_tuple) != 2:
            raise ValueError("Cannot convert {} to 2-tuple".format(
                repr(numerical_range)))

        floor, ceil = numerical_range_tuple

        floor = float(floor)
        ceil = float(ceil)

        if floor > ceil:
            raise ValueError(
                "Minimum of range ({}, {}) is greater than maximum".format(
                    floor, ceil))

        if self.minimum is not None and (floor < self.minimum
                                         or ceil < self.minimum):
            raise ValueError(
                "Minimum of range ({}, {}) is less than {}".format(
                    floor, ceil, self.minimum))

        if self.maximum is not None and (floor > self.maximum
                                         or ceil > self.maximum):
            raise ValueError(
                "Maximum of range ({}, {}) is greater than {}".format(
                    floor, ceil, self.maximum))

        return (floor, ceil)


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
