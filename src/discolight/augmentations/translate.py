"""An augmentation to translate an image."""
import numpy as np
from discolight.params.params import Params
from .bbox_utilities import bbox_utilities
from .augmentation.types import Augmentation, BoundedNumber
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Translate(Augmentation):

    """Translate the given image."""

    def __init__(self, translate_x, translate_y):
        """Construct a Translate augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.translate_x = translate_x
        self.translate_y = translate_y

        self.corner_x = 0
        self.corner_y = 0

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("translate_x", "", BoundedNumber(float, 0.0, 1.0),
                            0.2).add("translate_y", "",
                                     BoundedNumber(float, 0.0, 1.0), 0.2)

    def augment(self, img, bboxes):
        """Augment an image."""
        height, width, _ = img.shape
        translate_factor_x = self.translate_x
        translate_factor_y = self.translate_y
        canvas = np.zeros(img.shape).astype(np.uint8)
        corner_x = int(translate_factor_x * width)
        corner_y = int(translate_factor_y * height)
        orig_box_cords = [
            max(0, corner_y),
            max(corner_x, 0),
            min(height, corner_y + width),
            min(width, corner_x + width),
        ]
        mask = img[max(-corner_y, 0):min(width, -corner_y + height),
                   max(-corner_x, 0):min(width, -corner_x + width), :, ]
        canvas[orig_box_cords[0]:orig_box_cords[2],
               orig_box_cords[1]:orig_box_cords[3], :, ] = mask
        translated_img = canvas

        # code below transform the bboxes accordingly.
        bboxes[:, :4] = bboxes[:, :4] + [
            corner_x,
            corner_y,
            corner_x,
            corner_y,
        ]
        bboxes = bbox_utilities.clip_box(bboxes, [0, 0, width, height], 0.25)
        return translated_img, bboxes
