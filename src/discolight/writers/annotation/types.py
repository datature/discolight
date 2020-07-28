"""Base types for annotation writers."""
from abc import ABC, abstractmethod
import csv
from discolight.params.params import Params


class AnnotationWriter(ABC):

    """A class that saves annotation objects associated with images.

    Annotation writers can be used in a with context.
    """

    _include_in_factory = True

    @abstractmethod
    def __enter__(self):
        """Initialize the annotation writer."""
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
    def write_annotations_for_image(self, image_name, image, annotations):
        """Write the annotations for the given image.

        Annotations are passed as a list of unnormalized BoundingBox
        objects.
        """
        raise NotImplementedError


class CSVAnnotationWriter(AnnotationWriter):

    """An abstract CSV annotation writer.

    Concrete implementations of this class determine the columns and content
    of the CSV file by implementing the get_csv_fieldnames and get_csv_row
    methods. Normalization is taken care of for you.
    """

    def __init__(self, annotations_file, normalized):
        """Construct a new CSV annotation writer."""
        self.annotations_file = annotations_file
        self.normalized = normalized

        self.annotations_fp = None
        self.writer = None

    @abstractmethod
    def get_csv_fieldnames(self):
        """Return an array of strings with the field names of the CSV file."""
        raise NotImplementedError

    def __enter__(self):
        """Open the annotations_file for writing."""
        self.annotations_fp = open(self.annotations_file, "w", newline='')
        self.writer = csv.DictWriter(self.annotations_fp,
                                     self.get_csv_fieldnames())

        self.writer.writeheader()

        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotations_file."""
        self.annotations_fp.close()

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_file",
            "The path to the CSV file to write the annotations to", str, "",
            True
        ).add(
            "normalized",
            "whether the bounding box coordinates should be normalized before "
            "saving", bool, True)

    @abstractmethod
    def get_csv_row(self, image_name, image, annotation):
        """Return a CSV row for the given annotation and image.

        The row should be returned as a dictionary object where each field
        name returned in get_csv_fieldnames is defined as a key.
        """
        raise NotImplementedError

    def write_annotations_for_image(self, image_name, image, annotations):
        """Write the CSV rows for the given image and annotations."""
        for annotation in annotations:

            processed_annotation = annotation
            if self.normalized:
                height, width, _ = image.shape
                processed_annotation = annotation.normalize(width, height)

            self.writer.writerow(
                self.get_csv_row(image_name, image, processed_annotation))
