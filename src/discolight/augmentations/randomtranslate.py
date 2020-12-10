"""An augmentation to randomly rotate an image."""
import random
from discolight.params.params import Params
from .augmentation.types import Augmentation, NumericalRange
from .translate import Translate
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class RandomTranslate(Augmentation):

    """Randomly Translate the given image."""

    def __init__(self, translate_range):
        """Construct a RandomTranslate augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.translate_range = translate_range

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("translate_range",
                            "The translate range should be within 0 and 1",
                            NumericalRange(0, 1), (0.2, 0.2))

    def augment(self, img, bboxes):
        """Augment an image."""

        translate_factor_x = random.uniform(*self.translate_range)
        translate_factor_y = random.uniform(*self.translate_range)

        return Translate(translate_x=translate_factor_x,
                         translate_y=translate_factor_y).augment(img, bboxes)
