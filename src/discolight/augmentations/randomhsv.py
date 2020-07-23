import random
import numpy as np
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomHSV(ColorAugmentation):
    """Randomly shifts the color space of the given image"""
    def __init__(self, hue, saturation, brightness):
        super().__init__()

        self.hue = hue
        self.saturation = saturation
        self.brightness = brightness

    @staticmethod
    def params():
        return Params().add("hue", "", tuple,
                            (0, 0)).add("saturation", "", tuple,
                                        (0, 0)).add("brightness", "", tuple,
                                                    (0, 0))

    def augment_img(self, img, _bboxes):

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
