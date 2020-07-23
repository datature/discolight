from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import AnnotationWriter


@singleton
class AnnotationWriterLoader:
    def __init__(self):

        annotation_writers_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(annotation_writers_directory, __name__,
                                      AnnotationWriter)


def get_annotation_writer_set():

    return AnnotationWriterLoader().loader.get_object_set()


def make_annotation_writer_factory():

    return AnnotationWriterLoader().loader.make_object_factory()
