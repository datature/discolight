"""A YOLO Darknet annotation writer."""
import os
import shutil
from discolight.params.params import Params
from .types import AnnotationWriter


class YOLODarknet(AnnotationWriter):

    """A YOLO Darknet annotation writer."""

    def __init__(self, annotations_folder, clean_directory):
        """Construct a new YOLO Darknet annotation writer."""
        self.annotations_folder = annotations_folder
        self.clean_directory = clean_directory

    def __enter__(self):
        """Open the annotation writer for writing."""
        if os.path.isdir(self.annotations_folder) and self.clean_directory:
            shutil.rmtree(self.annotations_folder)

        if not os.path.isdir(self.annotations_folder):
            os.mkdir(self.annotations_folder)

        return self

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_folder", "the directory to save annotation files to",
            str, "", True).add(
                "clean_directory",
                "whether to forcibly ensure the output directory is empty",
                bool, True)

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotation writer."""

    def write_annotations_for_image(self, image_name, image, annotations):
        """Write the annotations for the given image."""
        image_name_no_ext = os.path.splitext(image_name)[0]

        image_height, image_width, _ = image.shape

        with open(
                os.path.join(self.annotations_folder,
                             "{}.txt".format(image_name_no_ext)),
                'w') as annotations_file:

            for annotation in annotations:

                normalized = annotation.normalize(image_width, image_height)
                width = normalized.x_max - normalized.x_min
                height = normalized.y_max - normalized.y_min

                annotations_file.write("{} {} {} {} {}\n".format(
                    normalized.class_idx, normalized.x_min, normalized.y_min,
                    width, height))
