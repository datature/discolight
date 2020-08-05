"""An augmentation that erases random parts of an image."""
import random
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation, NumericalRange
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomEraser(ColorAugmentation):

    """Randomly erase a rectangular area in the given image.

    The erased area is replaced with random noise.
    """

    def __init__(self, x_range, y_range):
        """Construct a RandomEraser augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()
        self.x_range = x_range
        self.y_range = y_range

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "x_range", "normalized x range for coordinates that may be erased",
            NumericalRange(0.0, 1.0), (0.0, 1.0)).add(
                "y_range",
                "normalized y range for coordinates that may be erased",
                NumericalRange(0.0, 1.0), (0.0, 1.0))

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        width, height, _ = img.shape[1], img.shape[0], img.shape[2]

        x_floor = width * self.x_range[0]
        x_ceil = width * self.x_range[1]

        y_floor = height * self.y_range[0]
        y_ceil = height * self.y_range[1]

        x_min, x_max = 1, 0  # force invalid coordinates
        while x_min >= x_max:
            x_min = int(random.uniform(x_floor, x_ceil))
            x_max = int(random.uniform(x_floor, x_ceil))

        y_min, y_max = 1, 0  # force invalid coordinates
        while y_min >= y_max:
            y_min = int(random.uniform(y_floor, y_ceil))
            y_max = int(random.uniform(y_floor, y_ceil))

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
