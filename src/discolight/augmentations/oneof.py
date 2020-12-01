"""An augmentation that performs a random augmentation on an image."""
import random
from discolight.params.params import Params
from .augmentation.types import Augmentation, augmentation_list
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class OneOf(Augmentation):

    """Perform a randomly selected augmentation on the given image."""

    def __init__(self, augmentations):
        """Construct a OneOf augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this construct directly if you know what you are doing.
        """
        super().__init__()

        self.augmentations = augmentations

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("augmentations", "", augmentation_list, [])

    def augment(self, img, bboxes):
        """Augment an image."""
        if len(self.augmentations) < 1:
            return img, bboxes

        selected_augmentation = self.augmentations[random.randint(
            0,
            len(self.augmentations) - 1)]

        return selected_augmentation.augment(img, bboxes)
