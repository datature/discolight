"""An augmentation to randomly rotate an image."""
import random
from discolight.params.params import Params
from .augmentation.types import Augmentation, NumericalRange
from .scale import Scale
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomScale(Augmentation):

    """Randomly scale the given image."""

    def __init__(self, scale_range):
        """Construct a RandomScale augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.scale_range = scale_range

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("scale_range",
                            "The scale range should be bigger than -1",
                            NumericalRange(-1), (0.2, 0.2))

    def augment(self, img, bboxes):
        """Augment an image."""
        scale_factor_x = random.uniform(*self.scale_range)
        scale_factor_y = random.uniform(*self.scale_range)

        return Scale(scale_x=scale_factor_x,
                     scale_y=scale_factor_y).augment(img, bboxes)
