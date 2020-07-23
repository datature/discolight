import numpy as np
from discolight.params.params import Params
from .augmentation.types import Augmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class VerticalFlip(Augmentation):
    """Vertically flips the given image"""
    @staticmethod
    def params():
        return Params()

    def augment(self, img, bboxes):
        vert_flip_img = img[::-1, :, :]

        height, _, _ = img.shape
        height_array = np.zeros((len(bboxes), 2))
        height_array.fill(height)
        bboxes[:, [1, 3]] = height_array - bboxes[:, [3, 1]]
        return vert_flip_img, bboxes
