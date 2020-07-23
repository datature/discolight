import random
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomEraser(ColorAugmentation):
    """
    Randomly erases a rectangular area in the given image, replacing it with
    random noise
    """
    def __init__(self, x_min, y_min, x_max, y_max):
        super().__init__()
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    @staticmethod
    def params():
        return Params().add("x_min", "", float,
                            0).add("y_min", "", float,
                                   0).add("x_max", "", float,
                                          -1).add("y_max", "", float, -1)

    def augment_img(self, img, bboxes):

        width, height, _ = img.shape[1], img.shape[0], img.shape[2]
        self.x_max = self.x_max if self.x_max >= 0 else width
        self.y_max = self.y_max if self.y_max >= 0 else height

        x_min, x_max = 1, 0  # force invalid coordinates
        while x_min >= x_max:
            x_min = int(random.uniform(self.x_min, self.x_max))
            x_max = int(random.uniform(self.x_min, self.x_max))

        y_min, y_max = 1, 0  # force invalid coordinates
        while y_min >= y_max:
            y_min = int(random.uniform(self.y_min, self.y_max))
            y_max = int(random.uniform(self.y_min, self.y_max))

        # here must be int, because if not img[eraser_width etc]
        # does not take in float or decimals.
        eraser_width = int(x_max - x_min)
        eraser_height = int(y_max - y_min)

        # Iterate and Apply Eraser
        for row_idx in range(y_min, y_min + eraser_height):
            for col_idx in range(x_min, x_min + eraser_width):
                img[row_idx, col_idx] = [
                    random.uniform(0, 255),
                    random.uniform(0, 255),
                    random.uniform(0, 255),
                ]
        return img
