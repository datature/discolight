"""Base types for annotation loaders."""
from abc import ABC, abstractmethod
import csv
from collections import namedtuple
from discolight.params.params import Params
from discolight.annotations import ImageWithAnnotations


class AnnotationLoader(ABC):

    """A class that loads annotation objects associated with images.

    Annotation loaders can be used in a with context.
    """

    _include_in_factory = True

    @abstractmethod
    def __enter__(self):
        """Initialize the annotation loader."""
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotation loader."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def params():
        """Return a Params object describing constructor parameters."""
        raise NotImplementedError

    @abstractmethod
    def load_annotated_images(self, image_loader):
        """Load annotations and images.

        The source of annotations should specify the image name that each
        annotation belongs to. The annotation loader should invoke the
        load_image method of the given image_loader to load all of the
        images specified in the annotations source.

        The loaded images and annotations should be returned in a
        dictionary where the image names are the keys, and the values
        are ImageWithAnnotations named tuple objects.
        """
        raise NotImplementedError


CSVRow = namedtuple('CSVRow', 'image_name bbox')


class CSVAnnotationLoader(AnnotationLoader):

    """An abstract CSV annotation loader.

    Concrete implementations of this class determine how the annotations
    and image names are loaded from the CSV file by implementing the
    get_csv_row method. Normalization is taken care of for you.
    """

    def __init__(self, annotations_file, normalized):
        """Construct a new CSV annotation loader."""
        self.annotations_file = annotations_file
        self.normalized = normalized

        self.annotations_fp = None

    def __enter__(self):
        """Open the annotations_file for reading."""
        self.annotations_fp = open(self.annotations_file, "r", newline='')
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotations_file."""
        self.annotations_fp.close()

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_file",
            "The path to the CSV file containing the annotations", str, "",
            True
        ).add(
            "normalized",
            "whether the bounding box coordinates are stored in a normalized "
            "format", bool, True)

    @abstractmethod
    def get_csv_row(self, row):
        """Return a CSVRow named tuple object from the given CSV row.

        The raw CSV row is passed as a dictionary object where the keys
        correspond to field names of the file. The CSVRow object must
        be constructed with the image name, and a BoundingBox object.
        """
        raise NotImplementedError

    def load_annotated_images(self, image_loader):
        """Load annotations and images from a CSV file."""
        images = {}

        reader = csv.DictReader(self.annotations_fp, skipinitialspace=True)

        for row in reader:

            csv_row = self.get_csv_row(row)

            if csv_row.image_name in images:
                if self.normalized:
                    height, width, _ = images[csv_row.image_name].image.shape

                    images[csv_row.image_name].bboxes.append(
                        csv_row.bbox.unnormalize(width, height))
                    continue

                images[csv_row.image_name].bboxes.append(csv_row.bbox)
                continue

            image = image_loader.load_image(csv_row.image_name)

            annotation = csv_row.bbox
            if self.normalized:
                height, width, _ = image.shape
                annotation = csv_row.bbox.unnormalize(width, height)

            images[csv_row.image_name] = ImageWithAnnotations(
                image=image_loader.load_image(csv_row.image_name),
                bboxes=[annotation])

        return images
