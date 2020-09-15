"""A YOLO Keras annotation loader."""
from discolight.params.params import Params
from discolight.annotations import BoundingBox, ImageWithAnnotations
from .types import AnnotationLoader


class YOLOKeras(AnnotationLoader):

    """A YOLO Keras annotation loader."""

    def __init__(self, annotations_file):
        """Construct a new YOLO Keras annotation loader."""
        self.annotations_file = annotations_file

        self.annotations_fp = None

    def __enter__(self):
        """Open the annotations_file for reading."""
        self.annotations_fp = open(self.annotations_file, "r")
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotations_file."""
        self.annotations_fp.close()

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_file",
            "The path to the TXT file containing the annotations", str, "",
            True)

    def load_annotated_images(self, image_loader):
        """Load annotations and images from a CSV file."""

        def parse_annotation(annotation_str):

            annotation_parts = annotation_str.split(",")

            if len(annotation_parts) != 5:
                raise ValueError(
                    "'{}' is not a valid annotation".format(annotation_str))

            x_min = float(annotation_parts[0])
            y_min = float(annotation_parts[1])
            x_max = float(annotation_parts[2])
            y_max = float(annotation_parts[3])
            class_idx = float(annotation_parts[4])

            return BoundingBox(x_min, y_min, x_max, y_max, class_idx)

        images = {}

        for line in self.annotations_fp:

            if len(line.strip()) < 1:
                continue

            line_parts = line.strip().split(" ")

            image_name = line_parts[0]
            image = image_loader.load_image(image_name)

            annotations = list(map(parse_annotation, line_parts[1:]))

            images[image_name] = ImageWithAnnotations(image, annotations)

        return images
