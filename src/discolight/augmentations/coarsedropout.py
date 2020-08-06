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

    def __init__(self, deleted_area, num_rectangles):
        super().__init__()
        self.deleted_area = deleted_area
        self.num_rectangles = num_rectangles

    @staticmethod
    def params():
        return Params().add("deleted_area", "", float,
                            0.1).add("num_rectangles", "", int,
                                     25)

    def augment_img(self, img, bboxes):

        width, height = img.shape[1], img.shape[0]
        self.deleted_area = self.deleted_area if \
            self.deleted_area <= 1 and self.deleted_area >= 0 else random.uniform(
                0, 1)
        self.num_rectangles = self.num_rectangles if \
            self.num_rectangles >= 10 and self.num_rectangles <= 100 else random.uniform(
                10, 100)

        eraser_area = width * height * self.deleted_area
        eraser_rectangle = int(
            eraser_area / self.num_rectangles)

        # here must be int, because if not img[eraser_width etc]
        # does not take in float or decimals.
        eraser_width = int(math.sqrt(eraser_rectangle))
        eraser_height = int(eraser_rectangle / eraser_width)

        # Iterate and Apply Eraser
        for _ in range(1, self.num_rectangles):
            x = int(random.uniform(0, width - eraser_width))
            y = int(random.uniform(0, height - eraser_height))

            for row_idx in range(y, y + eraser_height):
                for col_idx in range(x, x + eraser_width):
                    img[row_idx, col_idx] = [0, 0, 0]
        return img
