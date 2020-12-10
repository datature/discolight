"""An augmentation to randomly rotate an image."""
import random
from discolight.params.params import Params
from .augmentation.types import Augmentation, NumericalRange
from .shear import Shear
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomShear(Augmentation):

    """Randomly shear the given image."""

    def __init__(self, shear_range):
        """Construct a RandomShear augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.shear_range = shear_range

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("shear_range", "The shear range has no bounds",
                            NumericalRange(), (0.2, 0.2))

    def augment(self, img, bboxes):
        """Augment an image."""

        shear_factor = random.uniform(*self.shear_range)

        return Shear(shear_factor=shear_factor).augment(img, bboxes)
