from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import ImageLoader


@singleton
class ImageLoaderLoader:
    def __init__(self):

        image_loaders_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(image_loaders_directory, __name__,
                                      ImageLoader)


def get_image_loader_set():

    return ImageLoaderLoader().loader.get_object_set()


def make_image_loader_factory():

    return ImageLoaderLoader().loader.make_object_factory()
