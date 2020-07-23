import random
from ..augmentation.types import Augmentation


def accepts_probs(augmentation):
    """
    Adds a probs parameter to the given augmentation so that this
    augmentation may be randomly applied.
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
                float, 1.0).ensure(
                    lambda params: params["probs"] >= 0 and params["probs"] <=
                    1, "probs must be between 0 and 1")

        def augment(self, img, bboxes):

            if random.random() < self.probs:
                return self.augmentation.augment(img, bboxes)

            return img, bboxes

    AcceptsProbsAugmentation.__name__ = augmentation.__name__
    AcceptsProbsAugmentation.__doc__ = augmentation.__doc__

    return AcceptsProbsAugmentation
