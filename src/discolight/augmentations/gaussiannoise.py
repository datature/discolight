"""A Gaussian noise augmentation."""
import random
from math import floor
import numpy as np
from skimage.util import random_noise
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class GaussianNoise(ColorAugmentation):

    """Add gaussian noise to the given image."""

    def __init__(self, mean, variance):
        """Construct a GaussianNoise augmenation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()
        self.mean = mean
        self.variance = variance

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("mean", "", float, 0).add("variance", "", float,
                                                      0.01)

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        gaussian_noise = random_noise(
            img,
            mode="gaussian",
            seed=floor(random.random() * 1000000),
            clip=True,
            mean=self.mean,
            var=self.variance,
        )
        gaussian_noise_img = np.array(255 * gaussian_noise, dtype=np.uint8)
        return gaussian_noise_img
