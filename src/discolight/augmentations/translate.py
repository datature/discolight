import numpy as np
from discolight.params.params import Params
from .bbox_utilities import bbox_utilities
from .augmentation.types import Augmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Translate(Augmentation):
    """Translates the given image"""
    def __init__(self, translate_x, translate_y):
        super().__init__()

        self.translate_x = translate_x
        self.translate_y = translate_y

        self.corner_x = 0
        self.corner_y = 0

    @staticmethod
    def params():
        return Params().add("translate_x", "", float,
                            0.2).add("translate_y", "", float, 0.2).ensure(
                                lambda params: params["translate_x"] > 0 and
                                params["translate_x"] < 1,
                                "translate_x must be between 0 and 1").ensure(
                                    lambda params: params["translate_y"] > 0
                                    and params["translate_y"] < 1,
                                    "translate_y must be between 0 and 1")

    def augment(self, img, bboxes):

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
