"""An augmentation that randomly shifts an image's color space."""
import random
import numpy as np
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation, NumericalRange
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomHSV(ColorAugmentation):

    """Randomly shift the color space of the given image."""

    def __init__(self, hue, saturation, brightness):
        """Construct a RandomHSV augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.hue = hue
        self.saturation = saturation
        self.brightness = brightness

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("hue", "", NumericalRange(), (0.0, 0.0)).add(
            "saturation", "", NumericalRange(),
            (0.0, 0.0)).add("brightness", "", NumericalRange(), (0.0, 0.0))

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        hue = random.randint(*self.hue)
        saturation = random.randint(*self.saturation)
        brightness = random.randint(*self.brightness)
        img = img.astype(int)
        hsv_array = np.array([hue, saturation, brightness]).astype(int)
        img += np.reshape(hsv_array, (1, 1, 3))
        img = np.clip(img, 0, 255)
        img[:, :, 0] = np.clip(img[:, :, 0], 0, 179)
        img = img.astype(np.uint8)
        return img
