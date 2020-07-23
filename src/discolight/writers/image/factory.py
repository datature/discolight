from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import ImageWriter


@singleton
class ImageWriterLoader:
    def __init__(self):

        image_writers_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(image_writers_directory, __name__,
                                      ImageWriter)


def get_image_writer_set():

    return ImageWriterLoader().loader.get_object_set()


def make_image_writer_factory():

    return ImageWriterLoader().loader.make_object_factory()
