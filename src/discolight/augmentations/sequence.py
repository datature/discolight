"""An augmentation that performs a sequence of augmentations on an image."""
from discolight.params.params import Params
from .augmentation.types import Augmentation, augmentation_list
from .decorators.accepts_probs import accepts_probs


@accepts_probs
class Sequence(Augmentation):

    """Perform a sequence of augmentations on the given image."""

    def __init__(self, augmentations):
        """Construct a Sequence augmentation.

        You should probably use the augmentation factory or Discolight
        library interface to construct augmentations. Only invoke
        this constructor directly if you know what you are doing.
        """
        super().__init__()

        self.augmentations = augmentations

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("augmentations", "", augmentation_list, [])

    def augment(self, img, bboxes):
        """Augment an image."""
        for augmentation in self.augmentations:

            img, bboxes = augmentation.augment(img, bboxes)

        return img, bboxes
