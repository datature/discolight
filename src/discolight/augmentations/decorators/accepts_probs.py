"""Decorators for augmentations."""
import random
from ..augmentation.types import Augmentation, BoundedNumber


# yapf: disable
def accepts_probs(augmentation):
    """Add support for randomized application to an augmentation.

    Use this function as a decorator for augmentation classes. A probs
    parameter will be added to your augmentation that determines the
    probabililty of the augmentation being applied.
    """
    class AcceptsProbsAugmentation(Augmentation):

        # pylint: disable=protected-access
        _include_in_factory = augmentation._include_in_factory

        def __init__(self, probs=1.0, **params):
            super().__init__()
            self.__name__ = augmentation.__name__
            self.probs = probs
            self.augmentation = augmentation(**params)

        @staticmethod
        def params():
            return augmentation.params().add(
                "probs",
                "The probability that this augmentation will be applied",
                BoundedNumber(float, 0.0, 1.0), 1.0)

        def augment(self, img, bboxes):

            if random.random() < self.probs:
                return self.augmentation.augment(img, bboxes)

            return img, bboxes

    AcceptsProbsAugmentation.__name__ = augmentation.__name__
    AcceptsProbsAugmentation.__doc__ = augmentation.__doc__

    return AcceptsProbsAugmentation
# yapf: enable
