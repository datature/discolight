"""An augmentation to horizontally shear an image."""
import numpy as np
import cv2
from discolight.params.params import Params
from .augmentation.types import Augmentation
from .horizontalflip import HorizontalFlip
from .decorators.accepts_probs import accepts_probs


# TODO: Vertical Shear
@accepts_probs
class Shear(Augmentation):

    """Horizontally shear the given image."""

    def __init__(self, shear_factor):
        """Construct a Shear augmenation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.shear_factor = shear_factor

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("shear_factor", "", float, 0.2)

    def augment(self, img, bboxes):
        """Augment an image."""
        if self.shear_factor < 0:
            img, bboxes = HorizontalFlip().augment(img, bboxes)

        transformation_matrix = np.array([[1, abs(self.shear_factor), 0],
                                          [0, 1, 0]])
        new_width = img.shape[1] + abs(self.shear_factor * img.shape[0])
        bboxes[:, [0, 2]] = bboxes[:, [0, 2]] + (
            (bboxes[:, [1, 3]]) * abs(self.shear_factor)).astype(int)
        img = cv2.warpAffine(img, transformation_matrix,
                             (int(new_width), img.shape[0]))

        if self.shear_factor < 0:
            img, bboxes = HorizontalFlip().augment(img, bboxes)

        return img, bboxes
