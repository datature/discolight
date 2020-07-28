"""A factory for annotation writers."""
from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import AnnotationWriter


@singleton
class AnnotationWriterLoader:

    """A loader for all annotation writer objects."""

    def __init__(self):
        """Construct the annotation writer loader.

        Annotation writers are loaded from the modules in this directory.
        """
        annotation_writers_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(annotation_writers_directory, __name__,
                                      AnnotationWriter)


def get_annotation_writer_set():
    """Return the set of installed annotation writers.

    The set is returned as a dictionary where names of the annotation writers
    are the keys, and the annotation writer class objects are the values.
    """
    return AnnotationWriterLoader().loader.get_object_set()


def make_annotation_writer_factory():
    """Generate a factory function for constructing annotation writers.

    Invoke the returned factory function by passing the name of the
    annotation writer class you want to construct, followed by the
    parameters for the constructor as named arguments (e.g.,
    factory('FourCornersCSV', annotations_file=...)).
    """
    return AnnotationWriterLoader().loader.make_object_factory()
