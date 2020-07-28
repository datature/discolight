"""An augmentation to randomly rotate an image."""
import random
from discolight.params.params import Params
from .augmentation.types import Augmentation
from .rotate import Rotate
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomRotate(Augmentation):

    """Randomly rotate the given image."""

    def __init__(self, min_angle, max_angle):
        """Construct a RandomRotate augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.min_angle = min_angle
        self.max_angle = max_angle

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("min_angle", "", float, -10).add(
            "max_angle", "", float, 10).ensure(
                lambda params: params["min_angle"] < params["max_angle"],
                "min_angle must be less than max_angle")

    def augment(self, img, bboxes):
        """Augment an image."""
        angle = random.uniform(self.min_angle, self.max_angle)

        return Rotate(angle=angle).augment(img, bboxes)
