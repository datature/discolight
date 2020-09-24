"""A YOLO Keras annotation writer."""
from discolight.params.params import Params
from .types import AnnotationWriter


class YOLOKeras(AnnotationWriter):

    """A YOLO Keras annotation writer."""

    def __init__(self, annotations_file):
        """Construct a YOLO Keras annotation writer."""
        self.annotations_file = annotations_file

        self.annotations_fp = None

    def __enter__(self):
        """Open the annotations_file for writing."""
        self.annotations_fp = open(self.annotations_file, "w")
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annoations_file."""
        self.annotations_fp.close()

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_file",
            "The path to the TXT file to write the annotations to", str, "",
            True)

    def write_annotations_for_image(self, image_name, _image, annotations):
        """Write the annotations for the given image."""
        annotation_strs = [
            "{},{},{},{},{}".format(annot.x_min, annot.y_min, annot.x_max,
                                    annot.y_max, annot.class_idx)
            for annot in annotations
        ]

        self.annotations_fp.write("{} {}\n".format(image_name,
                                                   " ".join(annotation_strs)))
