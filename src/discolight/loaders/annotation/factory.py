"""A factory for annotation loaders."""
from pathlib import Path
from discolight.objectset.loader import ObjectSetLoader
from discolight.util.decorators import singleton
from .types import AnnotationLoader


@singleton
class AnnotationLoaderLoader:

    """A loader for all annotation loader objects."""

    def __init__(self):
        """Construct the annotation loader loader.

        Annotation loaders are loaed from the modules in this directory.
        """
        annotation_loaders_directory = Path(__file__).resolve().parent

        self.loader = ObjectSetLoader(annotation_loaders_directory, __name__,
                                      AnnotationLoader)


def get_annotation_loader_set():
    """Return the set of installed annotation loaders.

    The set is returned as a dictionary where names of the annotation loaders
    are the keys, and the annotation loader class objects are the values.
    """
    return AnnotationLoaderLoader().loader.get_object_set()


def make_annotation_loader_factory():
    """Generate a factory function for constructing annotation loaders.

    Invoke the returned factory function by passing the name of the annotation
    loader class you want to construct, followed by the parameters for the
    constructor as named arguments
    (e.g., factory('FourCornersCSV', annotations_file=...))
    """
    return AnnotationLoaderLoader().loader.make_object_factory()
