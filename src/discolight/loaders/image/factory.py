"""A factory for image loaders."""
from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import ImageLoader


@singleton
class ImageLoaderLoader:

    """A loader for all image loader objects."""

    def __init__(self):
        """Construct the image loader loader.

        Image loaders are loaded from the modules in this directory.
        """
        image_loaders_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(image_loaders_directory, __name__,
                                      ImageLoader)


def get_image_loader_set():
    """Return the set of installed image loaders.

    The set is returned as a dictionary where names of the image loaders are
    the keys, and the image loader class objects are the values.
    """
    return ImageLoaderLoader().loader.get_object_set()


def make_image_loader_factory():
    """Generate a factory function for constructing image loaders.

    Invoke the returned factory function by passing the name of the image
    loader class you want to construct, followed by the parameters for the
    constructor as named arguments
    (e.g., factory('Directory', directory=...)).
    """
    return ImageLoaderLoader().loader.make_object_factory()
