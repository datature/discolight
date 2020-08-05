"""An augmentation to scale an image."""
import cv2
import numpy as np
from discolight.params.params import Params
from .bbox_utilities import bbox_utilities
from .augmentation.types import Augmentation, BoundedNumber
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Scale(Augmentation):

    """Scale the given image."""

    def __init__(self, scale_x, scale_y):
        """Construct a Scale augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.scale_x = scale_x
        self.scale_y = scale_y

        self.resize_scale_x = 1 + self.scale_x
        self.resize_scale_y = 1 + self.scale_y

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("scale_x", "", BoundedNumber(float, -1.0),
                            0.2).add("scale_y", "", BoundedNumber(float, -1.0),
                                     0.2)

    def augment(self, img, bboxes):
        """Augment an image."""
        height, width, _ = img.shape
        resize_scale_x = 1 + self.scale_x
        resize_scale_y = 1 + self.scale_y
        resized_img = cv2.resize(img,
                                 None,
                                 fx=resize_scale_x,
                                 fy=resize_scale_y)
        canvas = np.zeros(img.shape, dtype=np.uint8)
        x_lim = int(min(resize_scale_x, 1) * width)
        y_lim = int(min(resize_scale_y, 1) * height)
        canvas[:y_lim, :x_lim, :] = resized_img[:y_lim, :x_lim, :]
        rescaled_img = canvas

        # code below transform the bboxes accordingly.
        bboxes[:, :4] = bboxes[:, :4] * [
            resize_scale_x,
            resize_scale_y,
            resize_scale_x,
            resize_scale_y,
        ]
        bboxes = bbox_utilities.clip_box(bboxes, [0, 0, 1 + width, height],
                                         0.25)
        return rescaled_img, bboxes
