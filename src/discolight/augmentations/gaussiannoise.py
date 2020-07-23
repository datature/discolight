import random
from math import floor
import numpy as np
from skimage.util import random_noise
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class GaussianNoise(ColorAugmentation):
    """Adds gaussian noise to the given image"""
    def __init__(self, mean, variance):
        super().__init__()
        self.mean = mean
        self.variance = variance

    @staticmethod
    def params():
        return Params().add("mean", "", float, 0).add("variance", "", float,
                                                      0.01)

    def augment_img(self, img, bboxes):

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
