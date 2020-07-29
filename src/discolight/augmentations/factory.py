"""A factory for image augmentations."""
from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .augmentation.types import Augmentation, augmentation_list


@singleton
class AugmentationLoader:

    """A loader for all augmentation objects."""

    def __init__(self):
        """Construct the augmentation loader.

        Augmentations are loaded from the modules in this directory.
        """
        augmentations_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(augmentations_directory, __name__,
                                      Augmentation)

        self.loader.bind_params_type_cast_to_factory_list(augmentation_list)


def get_augmentations_set():
    """Return the set of installed augmentations.

    The set is returned as a dictionary where names of the augmentations
    are the keys, and the augmentation class objects are the values.
    """
    return AugmentationLoader().loader.get_object_set()


def make_augmentations_factory():
    """Generate a factory function for constructing augmentations.

    Invoke the returned factory function by passing the name of the
    augmenation class you want to construct, followed by the parameters
    for the constructro as named arguments
    (e.g., factory('GrayScale', probs=0.7, ...)).
    """
    return AugmentationLoader().loader.make_object_factory()
