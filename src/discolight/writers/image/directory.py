"""An image writer that saves images to the local file system."""
import os
import shutil
import cv2
from discolight.params.params import Params
from .types import ImageWriter


class Directory(ImageWriter):

    """Writes images to a directory in the filesystem.

    Images will be saved to a file with the given name in the given directory.
    """

    def __init__(self, directory, clean_directory):
        """Construct a new Directory image writer."""
        self.directory = directory
        self.clean_directory = clean_directory

    def __enter__(self):
        """Initialize the image writer.

        The output directory is created or cleaned if necessary.
        """
        if os.path.isdir(self.directory) and self.clean_directory:
            shutil.rmtree(self.directory)

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the image writer."""

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "directory", "the directory to save images to", str, "", True).add(
                "clean_directory",
                "whether to forcibly ensure the output directory is empty",
                bool, True)

    def write_image(self, image_name, image):
        """Write an image with the given name to the output directory."""
        cc_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imwrite(os.path.join(self.directory, image_name), cc_image)
