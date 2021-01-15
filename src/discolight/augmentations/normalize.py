"""Normalize Images: This is extremely important if one decides to train on imagenet weights.
The code is with reference from Albumentations."""
import numpy as np
from discolight.params.params import Params
from .augmentation.types import Augmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Normalize(Augmentation):

    """Normalize an image. Divide pixel values by 255 = 2**8 - 1, subtract mean per channel and divide by std per channel."""

    def __init__(self, mean=, std=, max_pixel_value=255.0):

        super().__init__()

        self.mean = mean
        self.std = std
        self.max_pixel_value = max_pixel_value

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        
        return (
            Params()
            .add("mean", "", NumericalRange(), (0.485, 0.456, 0.406))
            .add("std", "", NumericalRange(), (0.229, 0.224, 0.225))
            # Note to user, it will not make sense to tune max_pixel_value to a too small value.
            .add("max_pixel_value", "", NumericalRange(), (0.0, 255.0))
        )

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        mean = np.array(self.mean, dtype=np.float32)
        mean *= self.max_pixel_value

        std = np.array(self.std, dtype=np.float32)
        std *= self.max_pixel_value

        denominator = np.reciprocal(std, dtype=np.float32)

        img = img.astype(np.float32)
        img -= mean
        img *= denominator
        return img
