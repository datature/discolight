"""A YOLO Darknet annotation loader."""
import glob
import os
import re
from discolight.params.params import Params
from discolight.annotations import BoundingBox, ImageWithAnnotations
from .types import AnnotationLoader


class YOLODarknet(AnnotationLoader):

    """A YOLO Darknet annotation loader."""

    def __init__(self, annotations_folder, image_ext):
        """Construct a new YOLO Darknet annotation loader."""
        self.annotations_folder = str(annotations_folder).rstrip(os.path.sep)
        self.image_ext = image_ext

    def __enter__(self):
        """Open the annotation loader."""
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotation loader."""

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("annotations_folder",
                            "The folder where the annotations are stored", str,
                            "",
                            True).add("image_ext",
                                      "The file extension for loaded images",
                                      str, "jpg")

    def load_annotated_images(self, image_loader):
        """Load annotations, images from a directory in YOLO Darknet format."""
        images = {}

        for annotation_filename in glob.glob(
                os.path.join(self.annotations_folder, "*.txt")):

            image_name_no_ext = re.match(
                rf"^{self.annotations_folder}{os.path.sep}(.+)\.txt$",
                annotation_filename).group(1)
            image_name = "{}.{}".format(image_name_no_ext, self.image_ext)

            annotations = []

            image = image_loader.load_image(image_name)

            height, width, _ = image.shape

            with open(annotation_filename, 'r') as annotation_file:

                for line in annotation_file:

                    if line.strip() == "":
                        continue

                    row = [
                        float(col)
                        for col in line.replace("\t", " ").split(" ")
                        if col != ""
                    ]

                    class_idx = int(row[0])
                    x_min = row[1]
                    y_min = row[2]
                    x_max = x_min + row[3]
                    y_max = y_min + row[4]

                    normalized = BoundingBox(x_min, y_min, x_max, y_max,
                                             class_idx)
                    unnormalized = normalized.unnormalize(width, height)

                    annotations.append(unnormalized)

            images[image_name] = ImageWithAnnotations(image, annotations)

        return images
