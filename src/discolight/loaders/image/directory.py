"""An image loader that loads images from the local filesystem."""
import os
from discolight.params.params import Params
from discolight.util.image import load_image
from .types import ImageLoader


class Directory(ImageLoader):

    """Load images from a directory in the filesystem.

    The image name from the AnnotationLoader will be used to fetch a file with
    the same name in the given directory.
    """

    def __init__(self, directory):
        """Construct a new Directory image loader."""
        self.directory = directory

    def __enter__(self):
        """Initialize the image loader."""
        return self

    def __exit__(self, _exc_type, _exc_vale, _exc_tb):
        """Close the image writer."""

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("directory",
                            "The directory from which to load images", str, "",
                            True)

    def load_image(self, image_name):
        """Load an image with the given name."""
        image_path = os.path.join(self.directory, image_name)

        return load_image(image_path)
