from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import AnnotationLoader


@singleton
class AnnotationLoaderLoader:
    def __init__(self):

        annotation_loaders_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(annotation_loaders_directory, __name__,
                                      AnnotationLoader)


def get_annotation_loader_set():

    return AnnotationLoaderLoader().loader.get_object_set()


def make_annotation_loader_factory():

    return AnnotationLoaderLoader().loader.make_object_factory()
