"""A horizontal flip augmentation."""
import numpy as np
from discolight.params.params import Params
from .augmentation.types import Augmentation
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class HorizontalFlip(Augmentation):

    """Horizontally flips the given image."""

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params()

    def augment(self, img, bboxes):
        """Augment an image."""
        hor_flip_img = img[:, ::-1, :]

        _, width, _ = img.shape
        width_array = np.zeros((len(bboxes), 2))
        width_array.fill(width)
        bboxes[:, [0, 2]] = width_array - bboxes[:, [2, 0]]
        return hor_flip_img, bboxes
