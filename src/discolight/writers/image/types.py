"""Base types for image writers."""
from abc import ABC, abstractmethod


class ImageWriter(ABC):

    """A class that saves augmented images.

    Image writers can be used in a with context.
    """

    _include_in_factory = True

    @abstractmethod
    def __enter__(self):
        """Initialize the image writer."""
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotation writer."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def params():
        """Return a Params object describing constructor parameters."""
        raise NotImplementedError

    @abstractmethod
    def write_image(self, image_name, image):
        """Write an image with the given name."""
        raise NotImplementedError
