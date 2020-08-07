"""An augmentation that adds random noise to an image."""
import random
from math import floor
from enum import Enum
import numpy as np
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation, BoundedNumber
from .decorators.accepts_probs import accepts_probs


class NoiseType(Enum):

    """The noise type to be applied in the SaltAndPepperNoise augmentation."""

    RGB = "RGB"
    SnP = "SnP"


@accepts_probs
class SaltAndPepperNoise(ColorAugmentation):

    """Add salt and pepper or RGB noise to the given image."""

    def __init__(self, replace_probs, pepper, salt, noise_type):
        """Construct a SaltAndPepperNoise augmenation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.replace_probs = replace_probs
        self.pepper = pepper
        self.salt = salt
        self.noise_type = noise_type

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("replace_probs", "", float,
                            0.1).add("pepper", "The color of the pepper",
                                     BoundedNumber(int, 0, 255),
                                     0).add("salt", "The color of the salt",
                                            BoundedNumber(int, 0, 255),
                                            255).add("noise_type",
                                                     "The type of noise",
                                                     NoiseType, "RGB")

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        np.random.seed(floor(random.random() * 1000000))

        if self.noise_type == NoiseType.SnP:
            random_matrix = np.random.rand(img.shape[0], img.shape[1])
            img[random_matrix >= (1 - self.replace_probs)] = self.salt
            img[random_matrix <= self.replace_probs] = self.pepper
        elif self.noise_type == NoiseType.RGB:
            random_matrix = np.random.rand(img.shape[0], img.shape[1],
                                           img.shape[2])
            img[random_matrix >= (1 - self.replace_probs)] = self.salt
            img[random_matrix <= self.replace_probs] = self.pepper
        return img
