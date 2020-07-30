"""An augmentation that adds sepia filter to an image."""
import numpy as np
from discolight.params.params import Params
from .augmentation.types import ColorAugmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Sepia(ColorAugmentation):

    """Returns a given image passed through the sepia filter."""

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params()

    def augment_img(self, img, _bboxes):
        """Augment an image."""
        sepia_img = np.zeros(img.shape)
        input_red, input_green, input_blue = (
            np.array(img[:, :, 0]),
            np.array(img[:, :, 1]),
            np.array(img[:, :, 2]),
        )
        # Formula taken from <https://www.techrepublic.com/blog/how-do-i/
        # how-do-i-convert-images-to-grayscale-and-sepia-tone-using-c/>
        red = (input_red * 0.393) + (input_green * 0.769) + (input_blue *
                                                             0.189)
        green = (input_red * 0.349) + (input_green * 0.686) + (input_blue *
                                                               0.168)
        blue = (input_red * 0.272) + (input_green * 0.534) + (input_blue *
                                                              0.131)

        sepia_img[:, :, 0] = red
        sepia_img[:, :, 1] = green
        sepia_img[:, :, 2] = blue

        sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)

        return sepia_img
