"""Base types for image loaders."""
from abc import ABC, abstractmethod


class ImageLoader(ABC):

    """A class that loads images.

    Image loaders can be used in a with context.
    """

    _include_in_factory = True

    @abstractmethod
    def __enter__(self):
        """Initialize the image loader."""
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the image loader."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def params():
        """Return a Params object describing constructor parameters."""
        raise NotImplementedError

    @abstractmethod
    def load_image(self, image_name):
        """Load an image with the given name.

        The image should be returned as an openCV image in HxWxC format, in
        RGB color space.
        """
        raise NotImplementedError
