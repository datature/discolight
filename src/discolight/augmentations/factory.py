from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .augmentation.types import Augmentation, augmentation_list


@singleton
class AugmentationLoader:
    def __init__(self):

        augmentations_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(augmentations_directory, __name__,
                                      Augmentation)

        self.loader.bind_params_type_cast_to_factory_list(augmentation_list)


def get_augmentations_set():
    """Returns the set of currently installed augmentations"""

    return AugmentationLoader().loader.get_object_set()


def make_augmentations_factory():
    """
    Returns a factory function that can be called to instantiate a new
    augmentation class from one of the augmentation classes present in this
    directory. Use this factory function as follows:


    .. code-block:: python

        factory = make_augmentations_factory()
        augmentation = factory('AugmentationName', param1=5, param2=10, ...)
    """

    return AugmentationLoader().loader.make_object_factory()
