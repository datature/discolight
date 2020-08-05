"""An augmentation that converts images to grayscale."""
import numpy as np
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class GrayScale(ColorAugmentation):

    """Return a grayscale version of the given image."""

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params()

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        grayscale_img = np.zeros(img.shape)
        red, green, blue = (
            np.array(img[:, :, 0]),
            np.array(img[:, :, 1]),
            np.array(img[:, :, 2]),
        )
        red, green, blue = red * 0.299, green * 0.587, blue * 0.114
        avg = red + green + blue
        grayscale_img = img
        for i in range(3):
            grayscale_img[:, :, i] = avg
        return grayscale_img
