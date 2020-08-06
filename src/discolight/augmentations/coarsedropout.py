import random
import math
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class CoarseDropout(ColorAugmentation):
    """
    Randomly erases a rectangular area in the given image.
    """

    def __init__(self, p, num):
        super().__init__()
        self.p = p
        self.num = num

    @staticmethod
    def params():
        return Params().add("p", "", float,
                            0.1).add("num", "", float,
                                     25)

    def augment_img(self, img, bboxes):

        width, height = img.shape[1], img.shape[0]
        self.p = self.p if self.p <= 1 and self.p >= 0 else random.uniform(
            0, 1)
        self.num = self.num if self.num >= 10 and self.num <= 100 else random.uniform(
            10, 100)

        eraser_area = width * height * self.p
        eraser_rectangle = int(
            eraser_area / self.num)

        # here must be int, because if not img[eraser_width etc]
        # does not take in float or decimals.
        eraser_width = int(math.sqrt(eraser_rectangle))
        eraser_height = int(eraser_rectangle / eraser_width)

        # Iterate and Apply Eraser
        for rect in range(1, self.num):
            x = int(random.uniform(0, width - eraser_width))
            y = int(random.uniform(0, height - eraser_height))
            for row_idx in range(y, y + eraser_height):
                for col_idx in range(x, x + eraser_width):
                    img[row_idx, col_idx] = [0, 0, 0]
        return img
