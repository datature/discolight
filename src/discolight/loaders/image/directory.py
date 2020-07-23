import os
from discolight.params.params import Params
from discolight.util.image import load_image
from .types import ImageLoader


class Directory(ImageLoader):
    """
    Loads images from a directory in the filesystem. The image name from the
    AnnotationLoader will be used to fetch a file with the same name in the
    given directory.
    """
    def __init__(self, directory):

        self.directory = directory

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        pass

    @staticmethod
    def params():
        return Params().add("directory",
                            "The directory from which to load images", str, "",
                            True)

    def load_image(self, image_name):

        image_path = os.path.join(self.directory, image_name)

        return load_image(image_path)
