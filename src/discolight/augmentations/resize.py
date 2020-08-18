"""A resize augmentation."""
from enum import Enum
import cv2
import numpy as np
from discolight.params.params import Params
from .augmentation.types import Augmentation, BoundedNumber
from .bbox_utilities.bbox_utilities import letterbox_image
from .decorators.accepts_probs import accepts_probs


class InterpolationType(Enum):

    """The interpolation type for resize."""

    INTER_NEAREST = "INTER_NEAREST"
    INTER_LINEAR = "INTER_LINEAR"
    INTER_AREA = "INTER_AREA"
    INTER_CUBIC = "INTER_CUBIC"
    INTER_LANCZOS4 = "INTER_LANCZOS4"


@accepts_probs
class Resize(Augmentation):

    """Resize an image without preserving aspect ratio."""

    def __init__(self, height, width, interpolation):
        """Construct a Resize augmenation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        self.height = height
        self.width = width
        self.interpolation = cv2.INTER_LINEAR

        if interpolation == InterpolationType.INTER_NEAREST:
            self.interpolation = cv2.INTER_NEAREST

        if interpolation == InterpolationType.INTER_AREA:
            self.interpolation = cv2.INTER_AREA

        if interpolation == InterpolationType.INTER_CUBIC:
            self.interpolation = cv2.INTER_CUBIC

        if interpolation == InterpolationType.INTER_LANCZOS4:
            self.interpolation = cv2.INTER_LANCZOS4

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("height", "The height of the resized image",
                            BoundedNumber(int, 0),
                            512).add("width", "the width of the resized image",
                                     BoundedNumber(int, 0),
                                     512).add("interpolation",
                                              "The interpolation type",
                                              InterpolationType,
                                              "INTER_LINEAR")

    def augment(self, img, bboxes):
        """Augment an image."""
        resized_img = cv2.resize(
            src=img,
            dsize=(self.width, self.height),
            interpolation=self.interpolation,
        )

        # code below transform the bboxes accordingly.

        height, width, _ = img.shape

        # get the scale of x and y respectively, for example if you
        # want to resize a 2000x1000 image into 1000 by 600, then on
        # the width side you need to scale down your bbox by 1000/2000
        # = 0.5 and on the height side you need to scale down your
        # bbox by 600/1000 = 0.6.

        x_scale, y_scale = self.width / width, self.height / height

        # change bboxes x_min and x_max coordinates by multiplying the x_scale
        # and cast it as int

        # change bboxes y_min and y_max coordinates by multiplying the y_scale
        # and cast it as int

        bboxes[:, [0, 2]] = (bboxes[:, [0, 2]] * x_scale).astype(int)
        bboxes[:, [1, 3]] = (bboxes[:, [1, 3]] * y_scale).astype(int)

        return resized_img, bboxes


@accepts_probs
class ResizeMaintainAspectRatio(Augmentation):

    """Resize an image while preserving aspect ratio."""

    def __init__(self, input_dim, interpolation):
        """Construct a ResizeMaintainAspectRatio augmenation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        self.input_dim = input_dim
        self.interpolation = cv2.INTER_LINEAR

        if interpolation == InterpolationType.INTER_NEAREST:
            self.interpolation = cv2.INTER_NEAREST

        if interpolation == InterpolationType.INTER_AREA:
            self.interpolation = cv2.INTER_AREA

        if interpolation == InterpolationType.INTER_CUBIC:
            self.interpolation = cv2.INTER_CUBIC

        if interpolation == InterpolationType.INTER_LANCZOS4:
            self.interpolation = cv2.INTER_LANCZOS4

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("input_dim",
                            "The new length of the shortest dimension",
                            BoundedNumber(int, 0),
                            512).add("interpolation", "The interpolation type",
                                     InterpolationType, "INTER_LINEAR")

    def augment(self, img, bboxes):
        """Augment an image."""
        width, height = img.shape[1], img.shape[0]

        img = letterbox_image(img, self.input_dim, self.interpolation)

        scale = min(self.input_dim / height, self.input_dim / width)
        bboxes[:, :4] = bboxes[:, :4] * scale

        new_width = scale * width
        new_height = scale * height

        del_h = (self.input_dim - new_height) / 2
        del_w = (self.input_dim - new_width) / 2

        add_matrix = np.array([[del_w, del_h, del_w, del_h]]).astype(int)

        bboxes[:, :4] = bboxes[:, :4] + add_matrix
        img = img.astype(np.uint8)

        return img, bboxes
