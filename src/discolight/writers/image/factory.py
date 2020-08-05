"""A factory for image writers."""
from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import ImageWriter


@singleton
class ImageWriterLoader:

    """A loader for all image writer objects."""

    def __init__(self):
        """Construct the image writer loader.

        Image writers are loaded from the modules in this directory.
        """
        image_writers_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(image_writers_directory, __name__,
                                      ImageWriter)


def get_image_writer_set():
    """Return the set of installed image writers.

    The set is returned as a dictionary where names of the image writers are
    the keys, and the image writer class objects are the values.
    """
    return ImageWriterLoader().loader.get_object_set()


def make_image_writer_factory():
    """Generate a factory function for constructing image writers.

    Invoke the returned factory function by passing the name of the image
    writer class you want to construct, followed by the parameters for
    the constructor as named arguments
    (e.g., factory('Directory', directory=...))
    """
    return ImageWriterLoader().loader.make_object_factory()
