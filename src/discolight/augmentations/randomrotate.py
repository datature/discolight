"""An augmentation to randomly rotate an image."""
import random
from discolight.params.params import Params
from .augmentation.types import Augmentation, NumericalRange
from .rotate import Rotate
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomRotate(Augmentation):

    """Randomly rotate the given image."""

    def __init__(self, angle_range):
        """Construct a RandomRotate augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.angle_range = angle_range

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "angle_range",
            "The range from which the random angle will be chosen",
            NumericalRange(-360.0, 360.0), (-10.0, 10.0))

    def augment(self, img, bboxes):
        """Augment an image."""
        angle = random.uniform(*self.angle_range)

        return Rotate(angle=angle).augment(img, bboxes)
