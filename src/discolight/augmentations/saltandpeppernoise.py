import random
from math import floor
import numpy as np
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class SaltAndPepperNoise(ColorAugmentation):
    """Adds salt and pepper or RGB noise to the given image"""
    def __init__(self, replace_probs, pepper, salt, noise_type):
        super().__init__()

        self.replace_probs = replace_probs
        self.pepper = pepper
        self.salt = salt
        self.noise_type = noise_type

    @staticmethod
    def params():
        return Params().add("replace_probs", "", float, 0.1).add(
            "pepper", "The color of the pepper", int,
            0).add("salt", "The color of the salt", int,
                   255).add("noise_type", "The type of noise (RGB or SnP)",
                            str, "RGB").ensure(
                                lambda params: params["noise_type"] == "RGB" or
                                params["noise_type"] == "SnP",
                                "noise_type must be RGB or SnP").ensure(
                                    lambda params: params[
                                        "salt"] >= 0 or params["salt"] <= 255,
                                    "salt must be between 0 and 255").ensure(
                                        lambda params: params["pepper"] >= 0 or
                                        params["pepper"] <= 255,
                                        "pepper must be between 0 and 255")

    def augment_img(self, img, _bboxes):

        np.random.seed(floor(random.random() * 1000000))

        if self.noise_type == "SnP":
            random_matrix = np.random.rand(img.shape[0], img.shape[1])
            img[random_matrix >= (1 - self.replace_probs)] = self.salt
            img[random_matrix <= self.replace_probs] = self.pepper
        elif self.noise_type == "RGB":
            random_matrix = np.random.rand(img.shape[0], img.shape[1],
                                           img.shape[2])
            img[random_matrix >= (1 - self.replace_probs)] = self.salt
            img[random_matrix <= self.replace_probs] = self.pepper
        return img
